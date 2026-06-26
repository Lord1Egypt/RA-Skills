# Cybernetic Evolver — 详细架构设计

## 1. 系统架构总览

```
┌──────────────────────────────────────────────────────────────────┐
│                      Cybernetic Evolver                           │
│                   （基于《工程控制论》的AI进化框架）                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │  感知模块   │    │  评价模块   │    │  决策模块   │          │
│  │ perceive()  │───▶│ evaluate()  │───▶│ decide()    │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│         │                  │                  │                 │
│         │                  │                  ▼                 │
│         │                  │          ┌─────────────┐          │
│         │                  │          │  执行模块   │          │
│         │                  │          │   act()     │          │
│         │                  │          └──────┬──────┘          │
│         │                  │                 │                  │
│         │          ┌──────┴──────┐          │                 │
│         │          │  反馈模块    │◀─────────┘                 │
│         │          │ feedback()   │                            │
│         │          └──────┬──────┘                            │
│         │                 │                                    │
│         ▼                 ▼                                    │
│  ┌─────────────┐    ┌─────────────┐                            │
│  │ 经验缓冲    │◀───│ 在线学习    │                            │
│  │buffer       │    │learner     │                            │
│  └─────────────┘    └─────────────┘                            │
│                             ▲                                   │
│                             │                                   │
│  ┌─────────────┐    ┌───────┴───────┐    ┌─────────────┐      │
│  │ 稳定性检查  │◀───│ 自适应调整   │───▶│ 结构变异    │      │
│  │ check()     │    │ adapt()      │    │mutate()     │      │
│  └─────────────┘    └──────────────┘    └─────────────┘      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 2. 核心模块设计

### 2.1 感知模块（Perception）

**职责**：将外部环境状态映射为系统内部特征向量。

```python
def perceive(self, raw_state) -> np.ndarray:
    """
    控制论对应: 系统辨识理论（《工程控制论》第三章）
    信息处理: 从噪声中提取本质信号
    """
    # 状态归一化
    normalized = (raw_state - self.state_mean) / (self.state_std + 1e-8)
    # 降维/特征提取（可选）
    if self.use_dimensionality_reduction:
        return self.pca.transform(normalized)
    return normalized
```

**关键特性**：
- 输入归一化（处理不同量纲的环境信号）
- 可选PCA/自动编码器降维
- 在线更新统计量（适应非平稳环境）

### 2.2 评价模块（Evaluation）

**职责**：实时计算当前策略表现与目标的误差。

```python
def evaluate(self) -> float:
    """
    控制论对应: 《工程控制论》第十八章"误差的控制"
    核心: J = target - performance（越小越好）
    """
    current = self.measure_performance()
    error = self.target - current
    return error
```

**误差类型**：
- **绝对误差**：|target - actual|
- **相对误差**：|target - actual| / |target|
- **二次误差**：(target - actual)^2（用于梯度计算）
- **积分误差**：∫|e(t)|dt（历史累积误差）

### 2.3 决策模块（Decision）

**职责**：在探索（Exploration）与利用（Exploitation）之间取得平衡。

```python
def decide(self, epsilon: float = None) -> int:
    """
    控制论对应: 《工程控制论》第十五章"最优控制"（多种策略的选择）
    探索-利用平衡: ε-greedy / UCB / 贝叶斯优化
    """
    if epsilon is None:
        epsilon = self.epsilon

    if random.random() < epsilon:
        return self.explore()   # 探索新策略
    else:
        return self.exploit()    # 利用已知最优
```

**探索方法**：
- `explore()`: 随机选择（纯探索）
- `explore_ucb()`: 上置信界算法（平衡探索与已知最优）
- `explore_boltzmann()`: 玻尔兹曼探索（基于softmax概率）

### 2.4 执行模块（Action）

**职责**：将决策输出的控制量作用于环境。

```python
def act(self, action: int) -> Tuple[np.ndarray, float, bool]:
    """
    控制论对应: 《工程控制论》第六章"随动系统"
    随动特性: 系统输出自动跟踪目标
    """
    # 动作映射
    control_signal = self.action_map[action]
    # 作用于环境
    next_state, reward, done = self.env.step(control_signal)
    return next_state, reward, done
```

### 2.5 反馈模块（Feedback）

**职责**：形成闭环，记录经验。

```python
def feedback(self, experience: Experience):
    """
    控制论对应: 维纳反馈控制原理（闭环反馈）
    形成完整闭环: 感知→评价→决策→执行→反馈→感知
    """
    self.experience_buffer.append(experience)
    # 更新在线学习模型
    self.online_learner.update(experience)
    # 检查稳定性
    if self.stability_check():
        self.adapt()
    else:
        self.rollback()
```

### 2.6 稳定性检查模块（Stability Check）

**职责**：Lyapunov稳定性判据，防止参数调整导致系统失稳。

```python
def stability_check(self) -> bool:
    """
    控制论对应: 自适应控制稳定性理论
    Popov超稳定性理论（《工程控制论》第十七章）
    
    Lyapunov函数: V(k) = e^2(k) + Σθ^2(k)
    稳定条件: ΔV = V(k+1) - V(k) < 0
    """
    error = self.evaluate()
    param_norm = np.linalg.norm(self.params)
    
    # Lyapunov函数值
    V = error**2 + self.lambda_reg * param_norm**2
    
    if not hasattr(self, 'V_prev'):
        self.V_prev = V
        return True
    
    delta_V = V - self.V_prev
    self.V_prev = V
    
    # ΔV < 0 表示稳定（误差和参数范数都在减小）
    if delta_V < self.delta_V_threshold:
        return True
    else:
        # 触发保护机制：拒绝本次参数更新
        self.rollback()
        return False
```

### 2.7 自适应调整模块（Adaptation）

**职责**：参数层的自适应调整（梯度下降/策略搜索）。

```python
def adapt(self):
    """
    控制论对应: 《工程控制论》第十七章"自适应控制"
    MIT方案: θ_dot = Gamma * e * phi
    梯度下降: θ <- θ - alpha * grad_J
    
    当参数调整无法恢复性能时，触发结构变异（mutate_structure）
    """
    error = self.evaluate()
    
    if abs(error) < self.adaptation_threshold:
        return  # 系统稳定，无需调整
    
    if self.use_gradient_based:
        # 梯度下降法（连续参数）
        gradient = self.compute_gradient()
        self.params -= self.learning_rate * gradient
    else:
        # 策略搜索法（离散/混合参数）
        self.policy_search()
    
    # 如果连续多次自适应失败，触发结构变异
    self.adaptation_failures += 1
    if self.adaptation_failures >= self.mutation_trigger:
        self.mutate_structure()
        self.adaptation_failures = 0
```

### 2.8 结构变异模块（Structure Mutation）

**职责**：策略拓扑层面的进化（突破局部最优）。

```python
def mutate_structure(self):
    """
    控制论对应: 1980年修订版"大系统理论"；协同学（哈肯）
    自组织系统: 为完成不同任务能自动重组结构
    
    钱学森预见: 控制论面临重要突破，系统越来越复杂，
    需要更高级的自组织能力
    
    变异类型:
    1. 添加新状态节点（扩展感知维度）
    2. 添加新动作选项（扩展行为空间）
    3. 重连边（改变因果关系）
    4. 删除冗余节点（结构简化）
    """
    mutation_type = random.choice(['add_node', 'add_action', 'rewire', 'prune'])
    
    if mutation_type == 'add_node':
        self.add_state_node()
    elif mutation_type == 'add_action':
        self.add_action_node()
    elif mutation_type == 'rewire':
        self.rewire_connections()
    elif mutation_type == 'prune':
        self.prune_redundant_nodes()
    
    # 变异后重新初始化相关参数
    self.reinitialize_affected_params()
```

## 3. 数据结构设计

### 3.1 经验（Experience）

```python
@dataclass
class Experience:
    """单条经验（控制论反馈环中的一个节点）"""
    state: np.ndarray         # 当前状态
    action: int               # 执行的动作
    reward: float             # 即时奖励
    next_state: np.ndarray    # 下一状态
    done: bool                # 是否终止
    timestamp: float          # 时间戳
    error: float              # 记录时的误差值
```

### 3.2 经验缓冲（ExperienceBuffer）

```python
class ExperienceBuffer:
    """
    经验缓冲（对应：人脑的记忆系统）
    控制论对应: 持续学习中的"经验积累"
    
    支持:
    - FIFO缓冲（容量固定）
    - 优先级回放（基于TD误差优先级）
    - 季风记忆（分离近期和远期经验）
    """
    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
    
    def append(self, exp: Experience): ...
    def sample(self, batch_size: int): ...
    def priority_sample(self, batch_size: int, top_k: float): ...
```

### 3.3 在线学习器（OnlineLearner）

```python
class OnlineLearner:
    """
    在线学习模块（对应：系统辨识的在线递推）
    控制论对应: 《工程控制论》系统辨识理论
    
    方法:
    - 递推最小二乘法（RLS）
    - 随机梯度下降（SGD）
    - 卡尔曼滤波（状态估计）
    """
    def update(self, experience: Experience): ...
    def predict(self, state: np.ndarray) -> float: ...
```

## 4. 分层进化机制

```
[元策略层] Meta-Strategy Layer
  │  目标函数定义、约束条件、全局评价标准
  │  进化周期: 慢（数百至数千个 episode）
  │
  ▼
[结构层]   Structure Layer  
  │  策略网络拓扑变化、状态空间重组
  │  进化触发: 参数调整连续失败
  │  进化周期: 中（数十至数百个 episode）
  │
  ▼
[参数层]   Parameter Layer  
  │  控制器增益、策略权重、阈值参数
  │  进化触发: 每步误差超阈值
  │  进化周期: 快（每个 time step）
  │
  ▼
[执行层]   Execution Layer
     即时控制、实时响应
     进化周期: 微秒级（每个 action）
```

### 分层进化协调

```python
def hierarchical_evolve(self):
    """
    分层递阶进化协调器
    高层进化指导低层方向，低层反馈影响高层决策
    """
    # 参数层：快速自适应
    if self.time_step % self.adaptation_interval == 0:
        self.adapt()
    
    # 结构层：中等频率变异
    if self.adaptation_failures >= self.mutation_trigger:
        self.mutate_structure()
    
    # 元策略层：低频目标调整
    if self.episode % self.meta_evolution_interval == 0:
        self.evolve_meta_strategy()
```

## 5. 稳定性保护机制

### 5.1 Lyapunov直接法

```python
def lyapunov_stability_check(self) -> bool:
    """
    直接Lyapunov法:
    V(e, θ) = e^2 + λ·||θ - θ*||^2
    
    其中:
    - e: 误差 (target - performance)
    - θ: 当前参数向量
    - θ*: 最优参数向量
    - λ: 权重系数
    
    稳定条件: ΔV = V(k+1) - V(k) ≤ 0
    如果 ΔV > 0 且超过阈值 → 拒绝更新，回滚参数
    """
    error = self.evaluate()
    param_deviation = np.linalg.norm(self.params - self.optimal_params)
    
    V_current = error**2 + self.lambda_reg * param_deviation**2
    
    if hasattr(self, 'V_history'):
        V_prev = self.V_history[-1]
        delta_V = V_current - V_prev
        
        if delta_V > self.lyapunov_threshold:
            # 不稳定，拒绝更新
            self.params = self.last_stable_params.copy()
            return False
    
    self.V_history.append(V_current)
    self.last_stable_params = self.params.copy()
    return True
```

### 5.2 Popov超稳定性判据

```python
def popov_stability_check(self) -> bool:
    """
    Popov超稳定性判据:
    用于自适应控制系统的稳定性分析
    
    条件:
    ∫₀ᵗ e(τ)r(τ)dτ ≥ -γ²  (对于某个 γ > 0)
    
    其中:
    - e: 误差信号
    - r: 参考模型输出
    
    如果条件被违反 → 系统可能失稳，触发保护
    """
    e = self.error_history
    r = self.reference_history
    
    integral = np.trapz(e * r, dx=self.dt)
    
    if integral < -self.gamma**2:
        # Popov判据被违反
        self.enter_protective_mode()
        return False
    
    return True
```

## 6. 探索-利用平衡策略

### 6.1 ε-greedy（默认）

```python
def epsilon_greedy(self, epsilon: float) -> int:
    if random.random() < epsilon:
        return random.randrange(self.action_dim)
    else:
        return np.argmax(self.Q_values)
```

### 6.2 UCB（Upper Confidence Bound）

```python
def ucb(self, c: float = 2.0) -> int:
    """
    UCB1公式:
    A_t = argmax [ Q(a) + c * sqrt(ln(t) / N(a)) ]
    
    其中:
    - Q(a): 动作a的估计价值
    - N(a): 动作a被选择的次数
    - t: 总选择次数
    - c: 探索常数
    """
    t = np.sum(self.action_counts) + 1
    ucb_values = self.Q_values + c * np.sqrt(np.log(t) / (self.action_counts + 1e-8))
    return np.argmax(ucb_values)
```

### 6.3 玻尔兹曼探索

```python
def boltzmann_explore(self, temperature: float = 1.0) -> int:
    """
    玻尔兹曼分布:
    P(a) = exp(Q(a)/T) / Σexp(Q(a)/T)
    
    T大 → 近似均匀随机（高探索）
    T小 → 接近贪心（高利用）
    """
    exp_values = np.exp(self.Q_values / temperature)
    probs = exp_values / np.sum(exp_values)
    return np.random.choice(self.action_dim, p=probs)
```

---

*架构版本: 1.0.0 | 最后更新: 2026-05-01*
