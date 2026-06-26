# CDA 实现指南（Implementation Guide）

> **配合**: CDA Code Lab 技能
> **作用**: 定义代码项目的结构、依赖、运行约定、质量标准

---

## 一、技术栈

| 组件 | 选型 | 版本要求 | 原因 |
|------|------|---------|------|
| 语言 | Python | ≥ 3.10 | 科学计算生态 |
| 深度学习框架 | PyTorch | ≥ 2.0 | 自动微分 + GPU |
| 数值计算 | NumPy | ≥ 1.24 | 张量基础操作 |
| 科学计算 | SciPy | ≥ 1.10 | ODE 求解器、稀疏矩阵 |
| 可视化 | Matplotlib | ≥ 3.7 | 轨迹绘图 |
| 数据处理 | Pandas | ≥ 2.0 | CSV/JSON 辅助 |
| 配置管理 | dataclasses | 标准库 | 无额外依赖 |

**不引入的依赖**（保持精简）：
- ❌ 不使用 TensorFlow/JAX（避免框架分散）
- ❌ 不使用 causal-learn NOTEARS 包（自行实现以控制细节）
- ❌ 不使用 gym/pygame（纯仿真，不涉及环境交互）

---

## 二、项目结构

Phase 1（热力学仿真引擎）的标准项目布局：

```
cda_thermal_sim/
├── README.md                  # 项目说明
├── requirements.txt           # pip 依赖
├── config.py                  # 全局配置（dataclass）
├── data/
│   ├── input/
│   │   └── *.graph.json       # Data Synthesizer 生成的输入数据
│   └── output/
│       └── *.trajectory.json  # 仿真输出轨迹
├── src/
│   ├── __init__.py
│   ├── entities.py            # EntityState, CausalEdge, WorldState 数据类
│   ├── data_loader.py         # JSON → Python 对象加载器
│   ├── mechanisms/
│   │   ├── __init__.py
│   │   ├── base.py            # MechanismFunction 抽象基类
│   │   ├── thermal.py         # 热力学机制函数（傅里叶/牛顿冷却）
│   │   ├── mechanical.py      # 力学机制函数（胡克/阻尼）
│   │   └── pinn.py            # PINN 通用机制函数
│   ├── integrator.py          # 辛积分器（Störmer-Verlet / Yoshida 4阶）
│   ├── hamiltonian.py         # 哈密顿投影模块
│   ├── cdablock.py            # CDABlock 完整管线
│   ├── learning/
│   │   ├── __init__.py
│   │   ├── bayesian_update.py # 贝叶斯状态更新（EKF）
│   │   ├── online_laplace.py  # 机制函数在线学习
│   │   └── notears.py         # NOTEARS 因果发现
│   └── utils.py               # 工具函数
├── tests/
│   ├── __init__.py
│   ├── test_entities.py       # 数据结构测试
│   ├── test_mechanisms.py     # 机制函数测试
│   ├── test_integrator.py     # 积分器测试
│   ├── test_hamiltonian.py    # 哈密顿投影测试
│   ├── test_cdablock.py       # 完整管线测试
│   └── test_energy.py         # 能量守恒验证
└── run_simulation.py          # 主入口
```

---

## 三、核心接口约定

### 3.1 EntityState 接口

```python
@dataclass
class EntityState:
    """CDA 实体状态。与 data-format-spec.md §2.1 一一对应。"""
    id: int
    name: str
    type: str               # thermal_node / mechanical_body / ...
    domain: str             # thermodynamics / mechanics / ...
    q: torch.Tensor          # 广义坐标 (dim_q,)
    p: torch.Tensor          # 共轭动量 (dim_p,)
    attributes: dict         # 固有属性
    belief_mean: torch.Tensor # 信念均值 (dim_q + dim_p,)
    belief_cov: torch.Tensor  # 信念协方差 (dim, dim)
```

**关键约定**：
- `q` 和 `p` 始终为 **1D Tensor**（即使单维度也是 shape `(1,)`，不是标量）
- 所有状态变量使用 **float64**（双精度），物理仿真对精度敏感
- `attributes` 中的数值参数也尽量使用 Tensor（便于自动微分）

### 3.2 CausalEdge 接口

```python
@dataclass
class CausalEdge:
    """CDA 因果边。与 data-format-spec.md §2.2 一一对应。"""
    source_id: int
    target_id: int
    mechanism: MechanismFunction  # 可微分因果机制函数
    mechanism_type: str
    strength: float           # α_ij ∈ [0, 1]
    delay: float              # τ_ij（秒）
    confidence: float         # 置信度 ∈ [0, 1]
```

### 3.3 MechanismFunction 接口

```python
class MechanismFunction(ABC):
    """因果机制函数抽象基类。
    
    每条因果边持有一个 MechanismFunction 实例。
    输入：source 实体状态 + target 实体状态
    输出：target 实体的状态变化量 Δs
    """

    @abstractmethod
    def forward(self, s_source: EntityState, s_target: EntityState) -> torch.Tensor:
        """计算因果影响。
        
        Args:
            s_source: 因端实体状态
            s_target: 果端实体状态
            
        Returns:
            delta_s: 状态变化量，shape 与 s_target.q + s_target.p 拼接一致
        """
        ...
    
    @abstractmethod
    def force(self, state: WorldState, entity_id: int) -> torch.Tensor:
        """计算作用在指定实体上的广义力（供辛积分器调用）。
        
        Args:
            state: 当前世界状态
            entity_id: 目标实体 ID
            
        Returns:
            F: 广义力，shape 与 entity.p 一致
        """
        ...
```

### 3.4 CDABlock 接口

```python
class CDABlock:
    """CDA 核心计算块。一次因果动力学步进的完整管线。
    
    管线流程（对应 CDA §3.2）：
    1. 因果路由（稀疏边选择）
    2. 机制计算（每条边计算 Δs）
    3. 辛积分（更新 q, p）
    4. 哈密顿投影（拉回能量流形）
    5. 贝叶斯更新（传播不确定性）
    """
    
    def step(self, state: WorldState, dt: float) -> WorldState:
        """执行一步因果动力学步进。
        
        Args:
            state: 当前世界状态 S_t
            dt: 时间步长
            
        Returns:
            next_state: 下一时刻世界状态 S_{t+1}
        """
        ...
```

---

## 四、运行约定

### 4.1 设备管理

```python
# config.py
@dataclass
class SimConfig:
    device: str = "cpu"          # 默认 CPU（物理仿真通常不需要 GPU）
    dtype: torch.dtype = torch.float64
    seed: int = 42
```

**GPU 使用原则**：
- 仿真本身通常在 CPU 上运行（实体数 < 10000 时）
- PINN 训练可使用 GPU
- 批量轨迹生成（蒙特卡洛采样）可使用 GPU 并行

### 4.2 数值精度要求

| 组件 | 精度要求 | 验证方法 |
|------|---------|---------|
| 辛积分器 | 局部误差 < 1e-6 | 与解析解对比 |
| 哈密顿投影 | 能量偏差 < tolerance | 每步检查 E(t) - E(0) |
| 贝叶斯更新 | 协方差矩阵正定 | Cholesky 分解检查 |
| NOTEARS | DAG 约束 h(W) < 1e-6 | 指数矩阵迹检查 |

### 4.3 随机种子与可复现性

```python
def set_seed(seed: int):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
```

所有仿真必须支持种子固定，确保结果可复现。

---

## 五、代码生成顺序

生成代码时，严格按以下顺序逐文件创建，每个文件完成后立即生成对应的测试：

```
1. config.py           →  无测试
2. src/entities.py     →  tests/test_entities.py
3. src/data_loader.py  →  tests/test_entities.py（扩展）
4. src/mechanisms/base.py      →  无测试（抽象类）
5. src/mechanisms/thermal.py   →  tests/test_mechanisms.py
6. src/integrator.py   →  tests/test_integrator.py
7. src/hamiltonian.py  →  tests/test_hamiltonian.py
8. src/cdablock.py     →  tests/test_cdablock.py + tests/test_energy.py
9. run_simulation.py   →  手动验证
```

**前置依赖规则**：后序文件可以导入前序文件，但不可反向依赖。

---

## 六、self-test 规范

每个组件的测试函数必须覆盖：

```python
def test_thermal_mechanism():
    """热传导机制函数测试。"""
    # 1. 正向传播：高温 → 低温，热流方向正确
    # 2. 平衡态：T_source == T_target → 热流为零
    # 3. 对称性：交换 source/target 改变热流符号
    # 4. 梯度检查：torch.autograd.gradcheck
    # 5. 数值精度：与解析傅里叶定律对比误差 < 1e-10
```

**必须通过的测试**：

| 测试 | 验证内容 | 通过条件 |
|------|---------|---------|
| energy_conservation | 长时间仿真的能量漂移 | \|E(t) - E(0)\| / E(0) < 0.001 |
| reversibility | 时间反演 (dt → -dt) 回到初态 | \|q(t) - q(0)\| < 1e-6 |
| causality | 因果边方向正确性 | 热量只从高温流向低温 |
| gradient_check | 自动微分一致性 | gradcheck error < 1e-5 |

---

## 七、依赖版本锁定

```
# requirements.txt
torch>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
pandas>=2.0.0
```

不锁定具体小版本号，仅规定最低版本。通过 `set_seed()` 保证可复现性，而非依赖版本锁定。
