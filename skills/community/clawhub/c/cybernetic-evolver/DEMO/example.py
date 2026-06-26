"""
CyberneticEvolver 演示示例

展示基于钱学森《工程控制论》的AI自我进化框架的三个典型场景。
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

# 添加CODE目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'CODE'))
from evolver import CyberneticEvolver, Experience


# ─────────────────────────────────────────────────────────────────────────────
# 示例1：简单函数优化（看不见的手）
# ─────────────────────────────────────────────────────────────────────────────

def demo_function_optimization():
    """
    场景：最大化一个简单函数 f(x) = -x² + 100
    
    展示 CyberneticEvolver 如何通过反馈+自适应找到目标函数的最优解。
    
    对应控制论概念:
    - 反馈：误差信号驱动参数调整
    - 自适应：参数自动向最优方向收敛
    - 稳定性：Lyapunov判据防止过冲
    """
    print("=" * 60)
    print("示例1：函数优化 — 寻找 f(x) = -x² + 100 的最大值")
    print("=" * 60)
    
    # 环境模拟器
    class FunctionEnv:
        def __init__(self):
            self.state_dim = 1
            self.action_dim = 101  # x ∈ [0, 100]
            self.best_x = 0
        
        def get_state(self):
            return np.array([self.best_x / 100.0])
        
        def step(self, action):
            x = action  # x ∈ [0, 100]
            reward = -x**2 + 100  # f(x) = -x² + 100，最大值在 x=0
            next_state = np.array([x / 100.0])
            return next_state, reward, False
        
        def get_performance(self):
            return -self.best_x**2 + 100
    
    env = FunctionEnv()
    
    evolver = CyberneticEvolver(
        target=100.0,  # 目标：最大化到100
        state_dim=1,
        action_dim=101,
        epsilon_start=1.0,
        epsilon_end=0.01,
        epsilon_decay=0.99,
        learning_rate=0.1,
        adaptation_threshold=5.0,
        mutation_trigger=20,
        env=env,
    )
    
    # 跟踪最优x
    best_x_record = []
    
    def track_best_x(evolver, env):
        best_action = evolver.exploit()
        env.best_x = best_action
        best_x_record.append(best_action)
    
    # 简单包装：在每步后更新环境的最优估计
    original_act = evolver.act
    def wrapped_act(action, state=None):
        result = original_act(action, state)
        best_action = evolver.exploit()
        env.best_x = best_action
        best_x_record.append(best_action)
        return result
    evolver.act = wrapped_act
    
    history = evolver.evolve(n_steps=500, verbose=True)
    
    # 绘制收敛曲线
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # 误差曲线
    axes[0, 0].plot(history['errors'])
    axes[0, 0].set_title('Error over Time')
    axes[0, 0].set_xlabel('Step')
    axes[0, 0].set_ylabel('Error (target - performance)')
    axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    # 探索率衰减
    axes[0, 1].plot(history['epsilon'])
    axes[0, 1].set_title('Exploration Rate (ε) Decay')
    axes[0, 1].set_xlabel('Step')
    axes[0, 1].set_ylabel('ε')
    
    # 最优动作收敛
    axes[1, 0].plot(best_x_record)
    axes[1, 0].axhline(y=0, color='g', linestyle='--', alpha=0.7, label='True optimum (x=0)')
    axes[1, 0].set_title('Best Action Found (x)')
    axes[1, 0].set_xlabel('Step')
    axes[1, 0].set_ylabel('x')
    axes[1, 0].legend()
    
    # Q值收敛
    final_Q = np.array(history['Q_values'][-1])
    axes[1, 1].bar(range(len(final_Q)), final_Q)
    axes[1, 1].set_title('Final Q-Values (Last Step)')
    axes[1, 1].set_xlabel('Action (x)')
    axes[1, 1].set_ylabel('Q-Value')
    
    plt.tight_layout()
    plt.savefig('/root/.openclaw/workspace/cybernetic-evolver/DEMO/demo1_convergence.png', dpi=150)
    print("收敛图已保存: demo1_convergence.png")
    
    return history


# ─────────────────────────────────────────────────────────────────────────────
# 示例2：环境突变适应（对应自稳定系统）
# ─────────────────────────────────────────────────────────────────────────────

def demo_environment_sudden_change():
    """
    场景：环境目标在运行中途发生突变
    
    展示：
    1. 系统初始收敛到旧目标
    2. 目标突变（对应《工程控制论》"环境条件发生剧烈变化"）
    3. 系统快速检测到突变（误差突然增大）
    4. 触发自适应调整，切换探索模式
    5. 重新收敛到新目标
    
    对应控制论概念:
    - 自稳定系统（《工程控制论》第十七章）
    - 适应性：系统自动改变结构参数应对环境变化
    - 反馈：误差突变触发紧急响应
    """
    print("\n" + "=" * 60)
    print("示例2：环境突变适应 — 从目标A切换到目标B")
    print("=" * 60)
    
    class ChangingTargetEnv:
        """目标在运行中途改变的环境"""
        def __init__(self):
            self.state_dim = 10  # Fixed dimension
            self.action_dim = 101  # x ∈ [0, 100]
            self.phase = 'A'
            self.phase_change_step = 300  # 在第300步时目标突变

        def get_state(self):
            return np.zeros(self.state_dim)  # State carries no info, action determines reward

        def step(self, action):
            # Phase A: 最优动作是50（奖励最高）
            # Phase B: 最优动作是90（奖励最高）
            if self.phase == 'A':
                optimal = 50
                target_reward = 100 - abs(action - optimal)
            else:
                optimal = 90
                target_reward = 100 - abs(action - optimal)

            # 奖励有一定噪声
            reward = target_reward + np.random.randn() * 2
            next_state = np.zeros(self.state_dim)
            return next_state, reward, False

        def get_performance(self):
            return 50.0  # Default intermediate value
    
    env = ChangingTargetEnv()
    
    evolver = CyberneticEvolver(
        target=100.0,
        state_dim=10,
        action_dim=101,
        epsilon_start=1.0,
        epsilon_end=0.01,
        epsilon_decay=0.995,
        learning_rate=0.1,
        adaptation_threshold=5.0,
        mutation_trigger=10,
        env=env,
    )
    
    history = {
        'errors': [],
        'performances': [],
        'epsilon': [],
        'phase': [],
    }
    
    n_steps = 600
    
    for step in range(n_steps):
        # 环境突变
        if step == 300:
            env.phase = 'B'
            evolver.epsilon = min(evolver.epsilon * 2.0, 0.5)  # 提高探索率应对变化
            print(f"\n>>> 环境突变！目标从A切换到B (Step {step})")
        
        # 标准循环
        raw_state = env.get_state()
        state = evolver.perceive(raw_state)
        current_perf = env.get_performance()
        error = evolver.evaluate(current_perf)
        action = evolver.decide()
        next_state, reward, done = evolver.act(action, state)
        
        exp = Experience(
            state=state,
            action=action,
            reward=reward,
            next_state=next_state,
            done=done,
            timestamp=step,
            error=error,
        )
        evolver.feedback(exp)
        
        if step % evolver.adaptation_interval == 0:
            evolver.adapt()
        
        evolver.decay_epsilon()
        
        history['errors'].append(error)
        history['performances'].append(current_perf)
        history['epsilon'].append(evolver.epsilon)
        history['phase'].append(env.phase)
        
        if step % 50 == 0:
            print(f"Step {step} | Phase: {env.phase} | ε: {evolver.epsilon:.3f} | "
                  f"Best action: {evolver.exploit()} | Error: {error:.2f}")
    
    # 绘制
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    steps = range(len(history['errors']))
    
    axes[0, 0].plot(steps, history['errors'], 'b-', linewidth=1)
    axes[0, 0].axvline(x=300, color='r', linestyle='--', alpha=0.7, label='Environment change')
    axes[0, 0].set_title('Error Over Time (with Environment Change)')
    axes[0, 0].set_xlabel('Step')
    axes[0, 0].set_ylabel('Error')
    axes[0, 0].legend()
    
    axes[0, 1].plot(steps, history['epsilon'], 'g-')
    axes[0, 1].axvline(x=300, color='r', linestyle='--', alpha=0.7)
    axes[0, 1].set_title('Exploration Rate')
    axes[0, 1].set_xlabel('Step')
    axes[0, 1].set_ylabel('ε')
    
    # 动作选择热力图
    Q_history = np.array([q[50] for q in [history['errors'][i] for i in range(len(history['errors']))]])
    
    axes[1, 0].scatter(range(len(history['performances'])), history['performances'], 
                       c=['red' if p == 'A' else 'blue' for p in history['phase']], 
                       alpha=0.5, s=10)
    axes[1, 0].axvline(x=300, color='r', linestyle='--', alpha=0.7)
    axes[1, 0].set_title('Performance (Red=A, Blue=B)')
    axes[1, 0].set_xlabel('Step')
    axes[1, 0].set_ylabel('Performance')
    
    axes[1, 1].text(0.5, 0.5, 
                     f"Environment Change at Step 300\n"
                     f"Phase A: Best action = 50\n"
                     f"Phase B: Best action = 90\n"
                     f"System re-adapted successfully",
                     ha='center', va='center', fontsize=14,
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('/root/.openclaw/workspace/cybernetic-evolver/DEMO/demo2_adaptation.png', dpi=150)
    print("\n适应图已保存: demo2_adaptation.png")
    
    return history


# ─────────────────────────────────────────────────────────────────────────────
# 示例3：探索-利用平衡收敛
# ─────────────────────────────────────────────────────────────────────────────

def demo_exploration_exploitation():
    """
    场景：展示 ε-greedy 策略如何随时间从探索转向利用
    
    对应控制论概念:
    - 《工程控制论》第十五章"最优控制"：多种控制策略的代价比较
    - 探索代价：尝试新策略消耗资源，可能降低短期性能
    - 利用代价：过度依赖已知策略可能陷入局部最优
    
    关键洞察：最优的探索-利用平衡是动态的，随系统对环境的了解程度调整
    """
    print("\n" + "=" * 60)
    print("示例3：探索-利用平衡 — ε-greedy 收敛过程")
    print("=" * 60)
    
    # 多臂老虎机环境
    class MultiArmedBandit:
        """简化的多臂老虎机"""
        def __init__(self, n_arms=10):
            self.n_arms = n_arms
            # 随机生成每个臂的真实期望奖励
            self.true_means = np.random.randn(n_arms) * 10
            self.best_arm = np.argmax(self.true_means)

        def get_state(self):
            return np.zeros(self.n_arms)  # 状态不携带信息

        def step(self, action):
            # 高斯噪声奖励
            reward = self.true_means[action] + np.random.randn() * 2
            return np.zeros(self.n_arms), reward, False

        def get_performance(self):
            return np.max(self.true_means)  # 最优奖励作为性能基准
    
    env = MultiArmedBandit(n_arms=10)
    print(f"最优臂: {env.best_arm}, 真实期望奖励: {env.true_means[env.best_arm]:.2f}")
    
    # 测试不同epsilon_decay的收敛速度
    decays = [0.99, 0.995, 0.999]
    colors = ['red', 'green', 'blue']
    
    all_histories = {}
    
    for decay in decays:
        print(f"\n测试 epsilon_decay = {decay}")
        
        evolver = CyberneticEvolver(
            target=env.true_means[env.best_arm],
            state_dim=env.n_arms,
            action_dim=env.n_arms,
            epsilon_start=1.0,
            epsilon_end=0.01,
            epsilon_decay=decay,
            learning_rate=0.1,
            adaptation_threshold=1.0,
            env=env,
        )
        
        history = evolver.evolve(n_steps=500, verbose=False)
        all_histories[decay] = history
        
        final_best = evolver.exploit()
        print(f"  最终找到的最优臂: {final_best} (真实最优: {env.best_arm})")
        print(f"  最终ε: {evolver.epsilon:.4f}")
        print(f"  最终Q值: {evolver.Q_values}")
    
    # 绘制收敛对比
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    for decay, color in zip(decays, colors):
        history = all_histories[decay]
        # 绘制累积 regrets（与最优的差距）
        regrets = [100 - p for p in history['performances']]
        axes[0, 0].plot(np.cumsum(regrets), color=color, label=f'decay={decay}', linewidth=1.5)
    
    axes[0, 0].set_title('Cumulative Regret (Lower is Better)')
    axes[0, 0].set_xlabel('Step')
    axes[0, 0].set_ylabel('Cumulative Regret')
    axes[0, 0].legend()
    
    for decay, color in zip(decays, colors):
        history = all_histories[decay]
        axes[0, 1].plot(history['epsilon'], color=color, label=f'decay={decay}', linewidth=1.5)
    
    axes[0, 1].set_title('Exploration Rate Over Time')
    axes[0, 1].set_xlabel('Step')
    axes[0, 1].set_ylabel('ε')
    axes[0, 1].legend()
    
    for decay, color in zip(decays, colors):
        history = all_histories[decay]
        axes[1, 0].plot(history['errors'], color=color, label=f'decay={decay}', linewidth=1.0, alpha=0.7)
    
    axes[1, 0].set_title('Error Over Time')
    axes[1, 0].set_xlabel('Step')
    axes[1, 0].set_ylabel('Error')
    axes[1, 0].legend()
    
    # 最终Q值对比
    for i, (decay, color) in enumerate(zip(decays, colors)):
        history = all_histories[decay]
        final_Q = history['Q_values'][-1]
        x_positions = np.arange(len(final_Q)) + i * 0.8
        axes[1, 1].bar(x_positions, final_Q, width=0.7, color=color, alpha=0.7, label=f'decay={decay}')
    
    axes[1, 1].axvline(x=env.best_arm, color='black', linestyle='--', alpha=0.7, label=f'True best arm={env.best_arm}')
    axes[1, 1].set_title('Final Q-Values (Arrow = True Optimal)')
    axes[1, 1].set_xlabel('Arm')
    axes[1, 1].set_ylabel('Q-Value')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('/root/.openclaw/workspace/cybernetic-evolver/DEMO/demo3_exploration.png', dpi=150)
    print("\n探索-利用对比图已保存: demo3_exploration.png")
    
    return all_histories


# ─────────────────────────────────────────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Cybernetic Evolver — 演示示例集")
    print("基于钱学森《工程控制论》的AI自我进化框架")
    print("=" * 60)
    
    # 确保输出目录存在
    os.makedirs('/root/.openclaw/workspace/cybernetic-evolver/DEMO', exist_ok=True)
    
    try:
        demo_function_optimization()
    except Exception as e:
        print(f"示例1出错: {e}")
    
    try:
        demo_environment_sudden_change()
    except Exception as e:
        print(f"示例2出错: {e}")
    
    try:
        demo_exploration_exploitation()
    except Exception as e:
        print(f"示例3出错: {e}")
    
    print("\n" + "=" * 60)
    print("所有演示完成！")
    print("输出目录: /root/.openclaw/workspace/cybernetic-evolver/DEMO/")
    print("=" * 60)
