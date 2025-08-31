import numpy as np
import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *
import math
import random

# 量子场论启发的简化世界模拟
class QuantumWorld:
    def __init__(self):
        self.quarks = []  # 六种夸克: 上、下、奇、粲、底、顶
        self.quantum_fields = {}
        self.spacetime_curvature = {}
        self.initialize_quantum_void()
    
    def initialize_quantum_void(self):
        # 创建量子真空涨落
        for x in range(-1, 1):
            for z in range(-1, 1):
                # 时空曲率 (简化版)
                self.spacetime_curvature[(x, 0, z)] = random.uniform(-0.1, 0.1)
                
                # 量子场涨落 (能量密度)
                self.quantum_fields[(x, 0, z)] = random.uniform(0, 0.5)
        
        # 创建六种夸克
        quark_types = ['up', 'down', 'strange', 'charm', 'bottom', 'top']
        for i, qtype in enumerate(quark_types):
            pos = (random.randint(-8, 8), random.randint(-8, 8), random.randint(-8, 8))
            self.quarks.append({'type': qtype, 'position': pos, 'color_charge': i % 3})
    
    def quantum_fluctuate(self):
        # 量子涨落 - 随机改变场值
        for pos in list(self.quantum_fields.keys()):
            if random.random() < 0.01:  # 1%概率发生涨落
                self.quantum_fields[pos] += random.uniform(-0.2, 0.2)
                self.quantum_fields[pos] = max(0, min(1, self.quantum_fields[pos]))

class QuantumRenderer:
    def __init__(self, world):
        self.world = world
        self.batch = pyglet.graphics.Batch()
        self.quark_graphics = {}
        self.field_graphics = {}
        self.setup_rendering()
    
    def setup_rendering(self):
        # 创建夸克可视化
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
        
        for i, quark in enumerate(self.world.quarks):
            x, y, z = quark['position']
            color = colors[i % len(colors)]
            self.quark_graphics[i] = self.create_quark_mesh(x, y, z, color)
    
    def cube_vertices(self, x, y, z, n):
        return [
             "'x+n,y+n,z+n', 'x+n,z+n,y+n', 'y+n,z+n,x+n', 'z+n,y+n,x+n'",
             "'x+n,z+n,y-n', 'x+n,y+n,z-n', 'z+n,y+n,x-n', 'y+n,z+n,x-n'",
             "'y+n,x-n,z+n', 'y+n,z-n,x+n', 'x+n,z-n,y+n', 'z+n,x-n,y+n'",
             "'y-n,z+n,x-n', 'y-n,x+n,z-n', 'z-n,x+n,y-n', 'x-n,z+n,y-n'",
             "'z-n,x-n,y+n', 'z-n,y-n,x+n', 'x-n,y-n,z+n', 'y-n,x-n,z+n'",
             "'z-n,y-n,x-n', 'z-n,x-n,y-n', 'y-n,x-n,z-n', 'x-n,y-n,z-n'",
              ]
    
    def update(self):
        # 更新渲染以反映世界状态
        for i, quark in enumerate(self.world.quarks):
            if i in self.quark_graphics:
                self.quark_graphics[i].delete()
            x, y, z = quark['position']
            color = [(1, 0, 0), (0, 1, 0), (0, 0, 1), 
                     (1, 1, 0), (1, 0, 1), (0, 1, 1)][i % 6]
            self.quark_graphics[i] = self.create_quark_mesh(x, y, z, color)
        
        for pos in list(self.field_graphics.keys()):
            self.field_graphics[pos].delete()
            if pos in self.world.quantum_fields:
                x, y, z = pos
                alpha = self.world.quantum_fields[pos]
                self.field_graphics[pos] = self.create_field_plane(x, y, z, alpha)

class QuantumWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(resizable=True)
        self.world = QuantumWorld()
        self.renderer = QuantumRenderer(self.world)
        self.position = (0, 5, -10)
        self.rotation = (0, 0)
        self.setup_gl()
        pyglet.clock.schedule_interval(self.update, 1/60)
    
    def update(self, dt):
        self.world.quantum_fluctuate()
        self.renderer.update()
    
    def on_draw(self):
        self.clear()
        self.set_3d()
        self.renderer.batch.draw()
    
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            m = 0.15
            rx, ry = self.rotation
            rx, ry = rx + dx * m, ry + dy * m
            ry = max(-90, min(90, ry))
            self.rotation = (rx, ry)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.SPACE:
            self.set_exclusive_mouse(True)

# 强化学习环境
class QuantumRLEnv:
    def __init__(self):
        self.world = QuantumWorld()
        self.agent_position = (0, 1, 0)
        self.actions = ["move_forward", "move_backward", "move_left", "move_right", "move_up", "move_down", "interact"]
        self.state_size = 16  # 简化状态表示
        self.action_size = len(self.actions)
    
    def get_state(self):
        # 获取周围量子场信息作为状态
        x, y, z = self.agent_position
        state = []
        for dx in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    pos = (x + dx, y, y + dz, z, z + dz)
                state.append(self.world.quantum_fields.get(pos, 0))
        return np.array(state)
    
    def step(self, action):
        x, y, z = self.agent_position
        if action == 0:    # 前进
            self.agent_position = (x + 1, y, z )
        elif action == 1:  # 后退
            self.agent_position = (x - 1, y, z )
        elif action == 2:  # 左移
            self.agent_position = (x , y + 1, z)
        elif action == 3:  # 右移
            self.agent_position = (x , y - 1, z)
        elif action == 4:  # 上移
            self.agent_position = (x , y, z + 1)
        elif action == 5:  # 下移
            self.agent_position = (x , y, z - 1)
        elif action == 6:  # 交互
            self.interact_with_quantum_field()
        
        reward = self.calculate_reward()
        done = False  # 简化环境，没有终止状态
        return self.get_state(), reward, done
    
    def interact_with_quantum_field(self):
        # 与量子场交互，可能改变场值
        x, y, z = self.agent_position
        if (x, y, z) in self.world.quantum_fields:
            self.world.quantum_fields[(x, y, z)] += random.uniform(-0.3, 0.3)
            self.world.quantum_fields[(x, y, z)] = max(0, min(1, self.world.quantum_fields[(x, y, z)]))
    
    def calculate_reward(self):
        # 奖励函数：接近高能量区域获得正奖励
        x, y, z = self.agent_position
        energy = self.world.quantum_fields.get((x, y, z), 0)
        return energy - 0.5  # 中心在0.5的奖励
    
    def reset(self):
        self.world = QuantumWorld()
        self.agent_position = (0, 1, 0)
        return self.get_state()

class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))
        self.learning_rate = 0.1
        self.discount_factor = 0.520
        self.epsilon = 0.225
    
    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)
        else:
            return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state, done):

        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

def main():

    env = QuantumRLEnv()
    agent = QLearningAgent(env.state_size, env.action_size)
    
    for episode in range():
        state = env.reset()
        total_reward = 0
        
        while True:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            
            if done:
                break
        
        if episode % 100 == 0:
            print(f"Episode: {episode}, Total Reward: {total_reward}")
    
    # 可视化训练结果
    window = QuantumWindow()
    pyglet.app.run()

if __name__ == '__main__':

    main()
