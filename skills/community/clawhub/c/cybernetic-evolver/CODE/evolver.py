"""
CyberneticEvolver — 基于钱学森《工程控制论》的AI自我进化框架

核心原理:
1. 闭环反馈驱动（Perceive → Evaluate → Decide → Act → Feedback）
2. 实时误差感知（evaluate() 实时计算性能误差）
3. 自适应参数调整（adapt() 基于梯度/策略搜索调整参数）
4. 探索-利用平衡（ε-greedy / UCB）
5. 分层递阶进化（参数层 → 结构层 → 元策略层）
6. 持续学习+稳定性保持（Lyapunov判据保护）

灵感来源:
- 钱学森《工程控制论》(1954/1980)
- 维纳《控制论》(1948)
- 协同学（哈肯，1970s）
- 自适应控制理论（MIT方案、Popov超稳定性）
- 耗散结构理论（普利高津，1969）
"""

import numpy as np
import random
from collections import deque
from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict, Any
import copy


# ─────────────────────────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Experience:
    """
    单条经验（控制论反馈环中的一个节点）
    
    对应《工程控制论》反馈控制中的"输入-输出对"：
    - state: 当前系统状态（输入）
    - action: 施加的控制量（控制输入）
    - reward: 系统响应（输出）
    - next_state: 下一时刻状态（新的输入）
    """
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool
    timestamp: float
    error: float  # 记录时的误差值，便于优先级回放


class ExperienceBuffer:
    """
    经验缓冲（对应：人脑的记忆系统 / 控制论中的历史数据存储）
    
    控制论对应:
    - 《工程控制论》"自我进化"章节：系统记忆操作细节
    - 持续学习中的"经验积累"
    
    支持:
    - FIFO缓冲（容量固定）
    - 优先级回放（基于TD误差）
    """
    
    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
        self.capacity = capacity
    
    def append(self, exp: Experience):
        """追加经验"""
        self.buffer.append(exp)
    
    def sample(self, batch_size: int) -> List[Experience]:
        """随机采样"""
        if len(self.buffer) < batch_size:
            return list(self.buffer)
        return random.sample(self.buffer, batch_size)
    
    def priority_sample(self, batch_size: int, top_k: float = 0.3) -> List[Experience]:
        """
        优先级采样：高误差经验优先回放
        
        控制论对应: 误差越大越需要重点学习（对应误差控制）
        """
        if len(self.buffer) <= batch_size:
            return list(self.buffer)
        
        # 按误差绝对值排序
        sorted_buffer = sorted(self.buffer, key=lambda e: abs(e.error), reverse=True)
        
        # 取top_k比例的高误差经验
        n_priority = max(1, int(len(sorted_buffer) * top_k))
        priority_pool = sorted_buffer[:n_priority]
        
        # 其余经验从普通池中随机采样
        remaining_pool = sorted_buffer[n_priority:]
        n_remaining = batch_size - min(len(priority_pool), batch_size // 2)
        
        selected = random.sample(priority_pool, min(len(priority_pool), batch_size // 2))
        if n_remaining > 0 and remaining_pool:
            selected.extend(random.sample(remaining_pool, n_remaining))
        
        return selected
    
    def __len__(self):
        return len(self.buffer)


class OnlineLearner:
    """
    在线学习模块（对应：系统辨识的在线递推估计）
    
    控制论对应:
    - 《工程控制论》第三章"输入、输出和传递函数"：系统参数在线辨识
    - 递推最小二乘法（RLS）/ 卡尔曼滤波
    
    功能: 每个时间步增量更新模型参数
    """
    
    def __init__(self, state_dim: int, learning_rate: float = 0.01):
        self.state_dim = state_dim
        self.alpha = learning_rate
        
        # 简单的线性模型参数（感知-评价映射）
        # 对应《工程控制论》中的"系统模型参数"
        self.weights = np.zeros(state_dim)
        self.bias = 0.0
    
    def update(self, experience: Experience):
        """
        在线更新模型参数（随机梯度下降）
        
        对应《工程控制论》中的"参数递推估计"
        """
        state = experience.state
        target = experience.reward
        
        # 预测
        prediction = np.dot(state, self.weights) + self.bias
        
        # 梯度
        error = target - prediction
        grad_w = error * state
        grad_b = error
        
        # 更新
        self.weights += self.alpha * grad_w
        self.bias += self.alpha * grad_b
    
    def predict(self, state: np.ndarray) -> float:
        """预测"""
        return np.dot(state, self.weights) + self.bias


class StabilityChecker:
    """
    稳定性检查器（对应：Lyapunov稳定性判据 + Popov超稳定性）
    
    控制论对应:
    - 《工程控制论》第十七章"自适应控制的稳定性"
    - Popov超稳定性理论（用于自适应控制系统的稳定性分析）
    
    Lyapunov函数: V(e, θ) = e^2 + λ·||θ - θ*||^2
    稳定条件: ΔV = V(k+1) - V(k) < 0
    """
    
    def __init__(self, lambda_reg: float = 0.1, delta_V_threshold: float = 0.0):
        self.lambda_reg = lambda_reg
        self.delta_V_threshold = delta_V_threshold  # ΔV阈值
        self.V_history = []
        self.last_stable_params = None
    
    def compute_lyapunov(self, error: float, params: np.ndarray, optimal_params: np.ndarray) -> float:
        """
        计算Lyapunov函数值
        
        V(e, θ) = e^2 + λ·||θ - θ*||^2
        
        对应《工程控制论》中的Lyapunov稳定性分析
        """
        param_deviation = np.linalg.norm(params - optimal_params)
        V = error**2 + self.lambda_reg * param_deviation**2
        return V
    
    def check(self, error: float, current_params: np.ndarray, optimal_params: np.ndarray) -> bool:
        """
        检查稳定性：ΔV < 0 表示稳定
        
        控制论对应: Lyapunov直接法稳定性判据
        """
        V_current = self.compute_lyapunov(error, current_params, optimal_params)
        
        if self.last_stable_params is None:
            self.last_stable_params = current_params.copy()
            self.V_history.append(V_current)
            return True
        
        V_prev = self.V_history[-1]
        delta_V = V_current - V_prev
        
        if delta_V <= self.delta_V_threshold:
            # 稳定：Lyapunov函数值不增加
            self.last_stable_params = current_params.copy()
            self.V_history.append(V_current)
            return True
        else:
            # 失稳：拒绝更新，回滚
            return False
    
    def reset(self):
        """重置历史"""
        self.V_history = []
        self.last_stable_params = None


# ─────────────────────────────────────────────────────────────────────────────
# 核心类
# ─────────────────────────────────────────────────────────────────────────────

class CyberneticEvolver:
    """
    基于钱学森《工程控制论》的AI自我进化框架
    
    钱学森在《工程控制论》中提出，控制系统必须具备：
    1. 反馈能力（闭环控制）
    2. 稳定性（自稳定系统）
    3. 自适应性（自适应控制）
    4. 学习能力（自学习系统）
    5. 自组织能力（自组织系统）
    
    本类将以上能力整合为可计算的进化算法。
    """
    
    def __init__(
        self,
        target: float,
        state_dim: int,
        action_dim: int,
        # 探索-利用平衡参数
        epsilon_start: float = 1.0,
        epsilon_end: float = 0.01,
        epsilon_decay: float = 0.995,
        # 学习参数
        learning_rate: float = 0.01,
        # 自适应参数
        adaptation_threshold: float = 1.0,
        adaptation_interval: int = 1,
        # 结构变异参数
        mutation_trigger: int = 10,
        # 稳定性参数
        lyapunov_lambda: float = 0.1,
        # 经验缓冲容量
        buffer_capacity: int = 10000,
        # 环境（可选，默认使用简单目标函数）
        env=None,
    ):
        """
        初始化
        
        Args:
            target: 目标值（对应《工程控制论》中的"期望输出"）
            state_dim: 状态维度
            action_dim: 动作选项数
            epsilon_start: 初始探索率
            epsilon_end: 最小探索率
            epsilon_decay: 探索率衰减因子
            learning_rate: 学习率（梯度下降步长）
            adaptation_threshold: 自适应触发阈值（误差大于此值时触发）
            adaptation_interval: 自适应执行间隔（每N步执行一次）
            mutation_trigger: 连续失败次数触发结构变异
            lyapunov_lambda: Lyapunov函数权重
            buffer_capacity: 经验缓冲容量
            env: 环境对象（需实现step()接口），默认使用内部简单环境
        """
        self.target = target
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # ── 探索-利用平衡 ──────────────────────────────────────────
        # 对应《工程控制论》第十五章"最优控制"：多种控制策略的选择
        self.epsilon = epsilon_start
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        
        # ── 学习参数 ────────────────────────────────────────────────
        self.learning_rate = learning_rate
        
        # ── 自适应参数 ───────────────────────────────────────────────
        self.adaptation_threshold = adaptation_threshold
        self.adaptation_interval = adaptation_interval
        self.adaptation_failures = 0
        
        # ── 结构变异参数 ─────────────────────────────────────────────
        # 对应《工程控制论》1980修订版"大系统理论"：自组织系统
        self.mutation_trigger = mutation_trigger
        self.structure_mutations = 0
        
        # ── 策略参数 ─────────────────────────────────────────────────
        # 对应《工程控制论》中的"控制器的增益参数"
        self.params = np.random.randn(state_dim) * 0.01
        self.optimal_params = np.zeros(state_dim)  # 渐近收敛目标
        self.last_stable_params = None
        
        # ── Q值表（用于探索-利用平衡）────────────────────────────────
        # 对应《工程控制论》中的"控制系统性能评价表"
        self.Q_values = np.zeros(action_dim)
        self.action_counts = np.zeros(action_dim)
        
        # ── 经验缓冲 ─────────────────────────────────────────────────
        self.experience_buffer = ExperienceBuffer(capacity=buffer_capacity)
        
        # ── 在线学习器 ──────────────────────────────────────────────
        self.online_learner = OnlineLearner(state_dim, learning_rate)
        
        # ── 稳定性检查器 ─────────────────────────────────────────────
        # 对应Lyapunov稳定性判据（Popov超稳定性）
        self.stability_checker = StabilityChecker(lambda_reg=lyapunov_lambda)
        
        # ── 环境 ─────────────────────────────────────────────────────
        if env is not None:
            self.env = env
        else:
            # 使用内置简单环境：状态空间是action_dim维one-hot，动作选择对应维度
            self.env = None
        
        self._state_mean = None  # Will be initialized on first perceive call

        # ── 统计 ─────────────────────────────────────────────────────
        self.time_step = 0
        self.episode = 0
        self.error_history = []
        
        # ── 元策略参数 ───────────────────────────────────────────────
        # 对应《工程控制论》中的"目标函数定义"
        self.meta_objective = "minimize_error"  # 或 "maximize_performance"
        self.meta_evolution_interval = 100  # 每N个episode检查一次元策略
    
    # ─────────────────────────────────────────────────────────────────────────
    # 核心接口
    # ─────────────────────────────────────────────────────────────────────────
    
    def perceive(self, state: np.ndarray) -> np.ndarray:
        """
        感知：环境状态 → 内部特征向量
        
        控制论对应:
        - 《工程控制论》第三章"输入、输出和传递函数"
        - 系统辨识：将外部状态映射为系统内部表示
        
        功能:
        1. 归一化处理（应对不同量纲的环境信号）
        2. 可选降维（PCA等）
        3. 在线更新统计量（适应非平稳环境）
        """
        # Ensure state is at least 1D
        state = np.atleast_1d(state).astype(float)
        
        if not hasattr(self, '_state_mean') or self._state_mean is None:
            self._state_mean = np.zeros(self.state_dim)
            self._state_std = np.ones(self.state_dim)
        
        # Match dimensions
        if len(self._state_mean) != len(state):
            self._state_mean = np.zeros(self.state_dim)
            self._state_std = np.ones(self.state_dim)
        
        # Online update statistics (exponential moving average)
        alpha = 0.01
        self._state_mean = (1 - alpha) * self._state_mean + alpha * state[:len(self._state_mean)]
        self._state_std = (1 - alpha) * self._state_std + alpha * (state[:len(self._state_std)]**2)
        self._state_std = np.sqrt(self._state_std + 1e-8)
        
        # Normalize
        normalized = (state[:len(self._state_mean)] - self._state_mean) / self._state_std
        
        return normalized
    
    def evaluate(self, current_performance: float = None) -> float:
        """
        评价：计算当前误差
        
        控制论对应:
        - 《工程控制论》第十八章"误差的控制"
        - 核心公式: error = target - performance
        
        功能: 实时量化系统表现，驱动后续决策和调整方向
        """
        if current_performance is None:
            # 如果没有提供，使用当前参数的预测值
            current_performance = self._predict_performance()
        
        error = self.target - current_performance
        self.error_history.append(error)
        
        return error
    
    def decide(self, epsilon: float = None) -> int:
        """
        决策：探索-利用平衡选择动作
        
        控制论对应:
        - 《工程控制论》第十五章"最优控制"
        - 多种控制策略的选择（探索新策略 vs 利用已知最优）
        
        策略: ε-greedy
        - rand() < ε → 探索（随机选择）
        - else → 利用（选择Q值最大的动作）
        """
        if epsilon is None:
            epsilon = self.epsilon
        
        if random.random() < epsilon:
            return self.explore()
        else:
            return self.exploit()
    
    def act(self, action: int, state: np.ndarray = None) -> Tuple[np.ndarray, float, bool]:
        """
        执行：将决策输出的控制量作用于环境
        
        控制论对应:
        - 《工程控制论》第六章"随动系统"
        - 随动特性：系统输出自动跟踪目标
        
        功能: 动作映射 → 环境交互 → 新状态获取
        """
        if self.env is not None:
            next_state, reward, done = self.env.step(action)
        else:
            # 内置简单环境：动作即状态维度
            # reward = 1.0 if action == self._true_action else 0.0
            # 简化为：性能 = 1.0 - abs(action - best_action) / action_dim
            best_action = self._get_best_action()
            reward = 1.0 if action == best_action else 0.0
            next_state = np.zeros(self.action_dim)
            next_state[action] = 1.0
            done = False
        
        # 更新Q值（采样平均）
        self._update_Q(action, reward)
        
        return next_state, reward, done
    
    def feedback(self, experience: Experience):
        """
        反馈：记录经验至缓冲，完成闭环
        
        控制论对应:
        - 维纳反馈控制原理（闭环反馈）
        - 形成完整闭环: 感知→评价→决策→执行→反馈→感知
        """
        # 写入经验缓冲
        self.experience_buffer.append(experience)
        
        # 在线学习模型更新
        self.online_learner.update(experience)
    
    def stability_check(self) -> bool:
        """
        稳定性检查：Lyapunov判据
        
        控制论对应:
        - 《工程控制论》第十七章"自适应控制的稳定性"
        - Popov超稳定性理论
        
        功能: 防止参数调整导致系统失稳（保护机制）
        """
        error = self.evaluate()
        
        # 使用Lyapunov函数值变化判断稳定性
        is_stable = self.stability_checker.check(
            error, self.params, self.optimal_params
        )
        
        if not is_stable:
            # 失稳保护：回滚参数
            if self.stability_checker.last_stable_params is not None:
                self.params = self.stability_checker.last_stable_params.copy()
                self.learning_rate *= 0.5  # 降低学习率
                self.learning_rate = max(self.learning_rate, 1e-5)
        
        return is_stable
    
    def adapt(self):
        """
        自适应：参数层调整（梯度下降/策略搜索）
        
        控制论对应:
        - 《工程控制论》第十七章"自适应控制"
        - MIT方案: θ_dot = Gamma * e * phi
        - 梯度下降: θ <- θ - α * grad_J
        
        触发条件: error ≥ adaptation_threshold
        """
        error = self.evaluate()
        
        if abs(error) < self.adaptation_threshold:
            # 系统稳定，无需调整
            self.adaptation_failures = 0
            return
        
        # 梯度下降（对应《工程控制论》中的参数自适应律）
        # gradient = ∂J/∂θ，简化用误差反向传导
        gradient = error * self.params / (np.linalg.norm(self.params) + 1e-8)
        
        new_params = self.params - self.learning_rate * gradient
        
        # 稳定性检查（防止过度调整导致失稳）
        # 对应Lyapunov稳定性保护
        error_before = abs(self.evaluate())
        self.params = new_params
        error_after = abs(self.evaluate())
        
        if error_after > error_before and error_before > self.adaptation_threshold:
            # 调整后误差变大，认为是一次"失败"
            self.adaptation_failures += 1
            # 回滚
            self.params = new_params + self.learning_rate * gradient
        else:
            # 调整有效
            self.adaptation_failures = 0
        
        # 检查是否需要触发结构变异
        if self.adaptation_failures >= self.mutation_trigger:
            self.mutate_structure()
            self.adaptation_failures = 0
    
    def mutate_structure(self):
        """
        结构变异：策略拓扑层面的进化
        
        控制论对应:
        - 《工程控制论》1980年修订版"大系统理论"
        - 协同学（哈肯）：自组织系统
        - 钱学森预见：控制论面临重要突破，需要更高级的自组织能力
        
        触发条件: 连续 adaptation_failures ≥ mutation_trigger 次
        
        变异类型:
        1. add_node: 添加新状态节点（扩展感知维度）
        2. add_action: 添加新动作选项（扩展行为空间）
        3. rewire: 重连边（改变因果关系）
        4. prune: 删除冗余节点（结构简化）
        """
        mutation_types = ['add_node', 'add_action', 'rewire', 'prune']
        mutation_type = random.choice(mutation_types)
        
        if mutation_type == 'add_node':
            # 添加一个随机新参数节点
            self.params = np.append(self.params, np.random.randn() * 0.01)
            self.optimal_params = np.append(self.optimal_params, 0.0)
            self.state_dim += 1
        
        elif mutation_type == 'add_action':
            # 添加新动作选项（扩展Q值表）
            self.Q_values = np.append(self.Q_values, 0.0)
            self.action_counts = np.append(self.action_counts, 0.0)
            self.action_dim += 1
        
        elif mutation_type == 'rewire':
            # 重连：打乱部分权重
            mask = np.random.rand(len(self.params)) < 0.3
            self.params[mask] = np.random.randn(np.sum(mask)) * 0.01
        
        elif mutation_type == 'prune' and len(self.params) > 1:
            # 删除最小幅度参数
            idx = np.argmin(np.abs(self.params))
            self.params = np.delete(self.params, idx)
            self.optimal_params = np.delete(self.optimal_params, idx)
            self.state_dim -= 1
        
        self.structure_mutations += 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # 辅助方法
    # ─────────────────────────────────────────────────────────────────────────
    
    def _predict_performance(self) -> float:
        """预测当前性能（用于evaluate无参数时）"""
        # 简化：性能 = dot(params, state_features) 归一化
        # 这里用均值
        if hasattr(self, '_state_mean') and self._state_mean is not None:
            features = self._state_mean
        else:
            features = np.zeros(self.state_dim)
        return np.dot(self.params, features)
    
    def _update_Q(self, action: int, reward: float):
        """更新Q值（采样平均）"""
        self.action_counts[action] += 1
        alpha = 1.0 / self.action_counts[action]
        self.Q_values[action] += alpha * (reward - self.Q_values[action])
    
    def explore(self) -> int:
        """探索：随机选择动作"""
        return random.randrange(self.action_dim)
    
    def exploit(self) -> int:
        """利用：选择Q值最大的动作"""
        return int(np.argmax(self.Q_values))
    
    def _get_best_action(self) -> int:
        """获取当前最优动作"""
        return int(np.argmax(self.Q_values))
    
    def measure_performance(self) -> float:
        """测量当前性能"""
        if self.env is not None:
            # 外部环境：通过环境接口获取
            return self.env.get_performance()
        else:
            # 内置环境：当前最佳Q值对应的预期奖励
            return np.max(self.Q_values)
    
    def decay_epsilon(self):
        """探索率衰减（ε-greedy策略的核心）"""
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 主循环
    # ─────────────────────────────────────────────────────────────────────────
    
    def evolve(self, n_steps: int, verbose: bool = True) -> Dict[str, Any]:
        """
        完整进化循环
        
        对应《工程控制论》的"自我进化系统":
        感知→评价→决策→执行→反馈→稳定性检查→自适应→结构变异
        
        Returns:
            Dict包含进化统计数据
        """
        history = {
            'errors': [],
            'performances': [],
            'epsilon': [],
            'Q_values': [],
            'structure_mutations': [],
            'adaptation_failures': [],
        }
        
        for step in range(n_steps):
            self.time_step = step
            
            # ── 感知 ─────────────────────────────────────────────────
            if self.env is not None:
                raw_state = self.env.get_state()
            else:
                # 内置环境：生成随机one-hot状态，隐藏最佳动作
                raw_state = np.zeros(self.action_dim)
                hidden_action = random.randrange(self.action_dim)
                raw_state[hidden_action] = 1.0
            
            state = self.perceive(raw_state)
            
            # ── 评价 ─────────────────────────────────────────────────
            current_performance = self.measure_performance()
            error = self.evaluate(current_performance)
            
            # ── 决策 + 执行 ─────────────────────────────────────────
            action = self.decide()
            next_state, reward, done = self.act(action, state)
            
            # ── 反馈 ─────────────────────────────────────────────────
            exp = Experience(
                state=state,
                action=action,
                reward=reward,
                next_state=next_state,
                done=done,
                timestamp=step,
                error=error,
            )
            self.feedback(exp)
            
            # ── 自适应（周期性）──────────────────────────────────────
            if step % self.adaptation_interval == 0:
                self.adapt()
            
            # ── 探索率衰减 ───────────────────────────────────────────
            self.decay_epsilon()
            
            # ── 记录历史 ─────────────────────────────────────────────
            history['errors'].append(error)
            history['performances'].append(current_performance)
            history['epsilon'].append(self.epsilon)
            history['Q_values'].append(self.Q_values.copy())
            history['structure_mutations'].append(self.structure_mutations)
            history['adaptation_failures'].append(self.adaptation_failures)
            
            if verbose and step % max(1, n_steps // 10) == 0:
                avg_error = np.mean(history['errors'][-max(1, n_steps//10):])
                print(f"Step {step}/{n_steps} | Error: {error:.4f} | Avg Error: {avg_error:.4f} | "
                      f"ε: {self.epsilon:.4f} | Mutations: {self.structure_mutations}")
        
        if verbose:
            print(f"\n=== Evolution Complete ===")
            print(f"Total steps: {n_steps}")
            print(f"Final error: {history['errors'][-1]:.4f}")
            print(f"Best error: {min(history['errors']):.4f}")
            print(f"Structure mutations: {self.structure_mutations}")
            print(f"Final Q-values: {self.Q_values}")
        
        return history
    
    def __repr__(self):
        return (f"CyberneticEvolver(target={self.target}, state_dim={self.state_dim}, "
                f"action_dim={self.action_dim}, epsilon={self.epsilon:.4f}, "
                f"mutations={self.structure_mutations})")

    # ─────────────────────────────────────────────────────────────────────────
    # 可注入的外部接口（支持 Skill-as-Module 集成模式）
    # ─────────────────────────────────────────────────────────────────────────

    def set_performance_metric(self, metric_fn):
        """
        注入外部性能度量函数（J函数）

        对应《工程控制论》第十八章"误差的控制"中的目标函数定义。
        外部 agent 可通过此接口注入自己定义的 J 函数，进化器据此驱动优化。

        Args:
            metric_fn: callable(state, action, result) -> float
                输入：当前状态、采取的动作、执行结果
                输出：性能度量值（越大表示表现越好）
                返回值会自动转为误差：error = target - metric_fn返回值

        Example:
            # news agent（财经）注入选股收益函数
            def j_stock_pick(state, action, result):
                return result['daily_return']  # 越大越好

            evolver.set_performance_metric(j_stock_pick)

            # programmer agent（开发）注入代码质量函数
            def j_code_quality(state, action, result):
                return 1.0 - 0.7*result['bug_count'] - 0.3*result['complexity']

            evolver.set_performance_metric(j_code_quality)
        """
        self._external_J = metric_fn

    def set_state_extractor(self, extractor_fn):
        """
        注入外部状态提取函数

        用于将 agent 的上下文（如对话历史、任务描述）转换为进化器可用的特征向量。

        Args:
            extractor_fn: callable(context) -> np.ndarray
                输入：agent 的上下文对象（dict）
                输出：特征向量（维度需与 state_dim 一致）

        Example:
            def extract_context(ctx):
                return np.array([
                    ctx.get('task_difficulty', 0),
                    ctx.get('time_remaining', 1.0),
                    ctx.get('success_rate', 0.5),
                ])

            evolver.set_state_extractor(extract_context)
        """
        self._state_extractor = extractor_fn

    def set_action_transformer(self, transformer_fn):
        """
        注入外部动作转换函数

        将进化器输出的离散动作（int）转换为 agent 可执行的具体操作。

        Args:
            transformer_fn: callable(action: int, context) -> Any
                输入：进化器输出的动作编号、当前上下文
                输出：agent 可执行的具体操作（如函数调用、策略选择）

        Example:
            def transform(action, ctx):
                strategies = ['aggressive', 'moderate', 'conservative']
                return strategies[action]

            evolver.set_action_transformer(transform)
        """
        self._action_transformer = transformer_fn

    def optimize(self, context: Dict[str, Any], n_iterations: int = 10) -> Dict[str, Any]:
        """
        优化入口（供外部 agent 调用）

        对应控制论的"闭环控制器"调用接口：
        1. 从 context 提取状态
        2. 由进化器选择动作
        3. 由外部执行并获取结果
        4. 注入 J 函数计算误差
        5. 执行自适应/变异

        Args:
            context: dict，外部 agent 的上下文（状态、执行历史等）
            n_iterations: 优化迭代次数（默认10次）

        Returns:
            dict，包含优化结果、最优动作、误差历史等
        """
        history = {
            'errors': [],
            'actions': [],
            'metrics': [],
        }

        for i in range(n_iterations):
            # 1. 提取状态
            if hasattr(self, '_state_extractor'):
                raw_state = self._state_extractor(context)
            else:
                # 默认：从context中提取数值型键值对
                raw_state = {k: v for k, v in context.items()
                             if isinstance(v, (int, float)) and k != 'last_result'}

            # 确保状态是numpy数组
            if isinstance(raw_state, dict):
                state = np.array([raw_state.get(k, 0) for k in sorted(raw_state.keys())])
            elif isinstance(raw_state, (list, tuple)):
                state = np.array(raw_state)
            else:
                state = np.atleast_1d(raw_state)

            state = self.perceive(state)

            # 2. 决策
            action = self.decide()

            # 3. 转换动作（如果注入了 transformer）
            if hasattr(self, '_action_transformer'):
                actual_action = self._action_transformer(action, context)
            else:
                actual_action = action

            # 4. 获取执行结果（外部提供或模拟）
            result = context.get('last_result', {'score': 0.5})

            # 5. 计算误差
            if hasattr(self, '_external_J'):
                metric_value = self._external_J(state, actual_action, result)
                error = self.target - metric_value
            else:
                # 默认误差
                error = result.get('score', 0.5) - self.target

            self.error_history.append(error)

            # 6. 构造经验并反馈
            next_state = state  # 简化版
            exp = Experience(
                state=state,
                action=action,
                reward=-error,  # 误差取负作为reward
                next_state=next_state,
                done=False,
                timestamp=i,
                error=error,
            )
            self.feedback(exp)

            # 7. 自适应
            if i % self.adaptation_interval == 0:
                self.adapt()

            # 记录
            history['errors'].append(error)
            history['actions'].append(actual_action)
            history['metrics'].append(result.get('score', 0.5))

        return {
            'best_action': history['actions'][np.argmin(history['errors'])],
            'best_error': min(history['errors']),
            'final_error': history['errors'][-1],
            'history': history,
        }

    # ─────────────────────────────────────────────────────────────────────────
    # 持久化与元控制接口
    # ─────────────────────────────────────────────────────────────────────────

    def save(self, filepath: str) -> None:
        """
        保存当前进化器状态到文件

        对应《工程控制论》"系统记忆"原理：进化结果需要持久化以便下次恢复。
        保存内容：Q值表、参数、epsilon、策略版本等

        Args:
            filepath: 保存路径（建议用 .json 或 .pkl）
        """
        import json

        state = {
            'Q_values': self.Q_values.tolist(),
            'action_counts': self.action_counts.tolist(),
            'params': self.params.tolist(),
            'optimal_params': self.optimal_params.tolist(),
            'epsilon': self.epsilon,
            'learning_rate': self.learning_rate,
            'structure_mutations': self.structure_mutations,
            'adaptation_failures': self.adaptation_failures,
            'time_step': self.time_step,
            'episode': self.episode,
            'error_history': self.error_history[-1000:],  # 只保留最近1000条
            'state_dim': self.state_dim,
            'action_dim': self.action_dim,
            'target': self.target,
            # 元学习参数（进化器自己的超参数）
            '_meta': {
                'epsilon_decay': self.epsilon_decay,
                'epsilon_start': self.epsilon_start,
                'epsilon_end': self.epsilon_end,
                'adaptation_threshold': self.adaptation_threshold,
                'adaptation_interval': self.adaptation_interval,
                'mutation_trigger': self.mutation_trigger,
                'lyapunov_lambda': self.stability_checker.lambda_reg,
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def load(self, filepath: str) -> None:
        """
        从文件加载进化器状态

        对应《工程控制论》"系统记忆恢复"：加载历史最优状态，继续优化。

        Args:
            filepath: 之前保存的文件路径
        """
        import json

        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)

        self.Q_values = np.array(state['Q_values'])
        self.action_counts = np.array(state['action_counts'])
        self.params = np.array(state['params'])
        self.optimal_params = np.array(state['optimal_params'])
        self.epsilon = state['epsilon']
        self.learning_rate = state['learning_rate']
        self.structure_mutations = state['structure_mutations']
        self.adaptation_failures = state['adaptation_failures']
        self.time_step = state['time_step']
        self.episode = state['episode']
        self.error_history = state['error_history']
        self.state_dim = state['state_dim']
        self.action_dim = state['action_dim']
        self.target = state['target']

        # 元学习参数
        meta = state.get('_meta', {})
        self.epsilon_decay = meta.get('epsilon_decay', self.epsilon_decay)
        self.epsilon_start = meta.get('epsilon_start', self.epsilon_start)
        self.epsilon_end = meta.get('epsilon_end', self.epsilon_end)
        self.adaptation_threshold = meta.get('adaptation_threshold', self.adaptation_threshold)
        self.adaptation_interval = meta.get('adaptation_interval', self.adaptation_interval)
        self.mutation_trigger = meta.get('mutation_trigger', self.mutation_trigger)
        self.stability_checker.lambda_reg = meta.get('lyapunov_lambda', self.stability_checker.lambda_reg)

    def get_best_strategy(self) -> Dict[str, Any]:
        """
        获取当前最优策略

        供外部 agent 直接使用当前已找到的最优动作和参数。

        Returns:
            dict: {
                'best_action': int,           # 最优动作编号
                'best_action_name': str,       # 转换后的动作名称（如果有transformer）
                'Q_values': np.ndarray,        # 各动作Q值
                'confidence': float,           # 置信度（探索率越低越可信）
                'epsilon': float,              # 当前探索率
                'strategy_version': int,       # 策略版本（每次mutate_structure递增）
            }
        """
        best_action = int(np.argmax(self.Q_values))
        confidence = 1.0 - self.epsilon  # epsilon低=置信度高

        best_action_name = None
        if hasattr(self, '_action_transformer'):
            try:
                best_action_name = self._action_transformer(best_action, {})
            except Exception:
                best_action_name = str(best_action)

        return {
            'best_action': best_action,
            'best_action_name': best_action_name,
            'Q_values': self.Q_values.copy(),
            'confidence': float(confidence),
            'epsilon': self.epsilon,
            'strategy_version': self.structure_mutations + 1,
            'total_errors': len(self.error_history),
            'recent_avg_error': float(np.mean(self.error_history[-10:])) if self.error_history else None,
        }

    def history(self, last_n: int = None) -> Dict[str, Any]:
        """
        获取优化历史

        用于分析趋势、判断是否需要触发优化、评估当前状态。

        Args:
            last_n: 只返回最近N条误差历史，默认全部

        Returns:
            dict: {
                'errors': list[float],         # 误差历史
                'recent_avg_error': float,     # 最近平均误差
                'best_error': float,           # 历史最优误差
                'total_mutations': int,        # 总变异次数
                'total_steps': int,            # 总步数
                'is_converging': bool,         # 是否在收敛（最近10步误差趋势下降）
                'recommendation': str,          # 建议（继续优化/已收敛/需要变异）
            }
        """
        errors = self.error_history[-last_n:] if last_n else self.error_history

        if not errors:
            return {
                'errors': [],
                'recent_avg_error': None,
                'best_error': None,
                'total_mutations': self.structure_mutations,
                'total_steps': self.time_step,
                'is_converging': False,
                'recommendation': '无历史数据，请先运行optimize()或evolve()',
            }

        recent = errors[-10:] if len(errors) >= 10 else errors
        recent_avg = float(np.mean(recent))
        best_error = float(min(errors))

        # 判断收敛：最近10步误差趋势
        if len(recent) >= 5:
            slope = (recent[-1] - recent[0]) / len(recent)
            is_converging = slope < 0  # 斜率为负=误差在下降=收敛中
        else:
            is_converging = False

        # 建议
        if recent_avg > 0.5:
            recommendation = '误差仍高，建议继续优化或调整J函数'
        elif is_converging:
            recommendation = '正在收敛，保持当前策略'
        elif self.structure_mutations == 0 and len(errors) > 50:
            recommendation = '参数收敛但无结构变异，可尝试触发mutate_structure()探索'
        else:
            recommendation = '已收敛，当前策略为较优'

        return {
            'errors': errors,
            'recent_avg_error': recent_avg,
            'best_error': best_error,
            'total_mutations': self.structure_mutations,
            'total_steps': self.time_step,
            'is_converging': is_converging,
            'recommendation': recommendation,
        }

    def set_trigger_condition(self, trigger_fn):
        """
        注入触发条件判断函数

        当外部 agent 调用时，可先调用此函数判断是否需要真正执行优化。

        对应《工程控制论》"稳态判决"原理：不是每次都优化，而是条件触发。

        Args:
            trigger_fn: callable(performance_history: list[float]) -> dict
                输入：最近N次性能值列表
                输出：dict {
                    'should_optimize': bool,   # 是否需要优化
                    'reason': str,             # 原因说明
                    'suggested_iterations': int, # 建议迭代次数
                }

        Example:
            def check_trigger(perf_history):
                if len(perf_history) < 3:
                    return {'should_optimize': False, 'reason': '数据不足', 'suggested_iterations': 0}
                
                recent = perf_history[-3:]
                if all(recent[i] > recent[i+1] for i in range(len(recent)-1)):
                    return {'should_optimize': True, 'reason': '性能连续下降', 'suggested_iterations': 20}
                
                return {'should_optimize': False, 'reason': '性能稳定', 'suggested_iterations': 0}

            evolver.set_trigger_condition(check_trigger)
        """
        self._trigger_fn = trigger_fn

    def check_trigger(self, performance_history: list) -> Dict[str, Any]:
        """
        判断是否需要触发优化（供外部调用）

        Args:
            performance_history: 最近N次性能值

        Returns:
            dict: {
                'should_optimize': bool,
                'reason': str,
                'suggested_iterations': int,
            }
        """
        if hasattr(self, '_trigger_fn'):
            return self._trigger_fn(performance_history)
        else:
            # 默认：性能下降就优化
            if len(performance_history) >= 3:
                recent = performance_history[-3:]
                if all(recent[i] > recent[i+1] for i in range(len(recent)-1)):
                    return {
                        'should_optimize': True,
                        'reason': '性能连续3次下降（默认策略）',
                        'suggested_iterations': 20,
                    }
            return {
                'should_optimize': False,
                'reason': '性能稳定或数据不足',
                'suggested_iterations': 0,
            }

