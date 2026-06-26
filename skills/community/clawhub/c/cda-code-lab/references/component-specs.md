# CDA 组件接口规格（Component Specifications）

> **配合**: `implementation-guide.md`
> **作用**: 每个可生成组件的完整接口签名、输入输出规格、实现要点

---

## 一、核心数据类

### 1.1 EntityState

**文件**: `src/entities.py`

```python
@dataclass
class EntityState:
    id: int
    name: str
    type: str                          # 实体类型标识
    domain: str                        # 物理域
    q: torch.Tensor                    # 广义坐标 (dim_q,)
    p: torch.Tensor                    # 共轭动量 (dim_p,)
    attributes: dict                   # 固有属性（数值用 Tensor）
    belief_mean: torch.Tensor          # 信念均值 (dim_q + dim_p,)
    belief_cov: torch.Tensor           # 协方差矩阵 (dim, dim) 正定

    @property
    def state_dim(self) -> int:
        """总状态维度 = dim_q + dim_p"""
        return self.q.shape[0] + self.p.shape[0]

    def full_state(self) -> torch.Tensor:
        """拼接 q 和 p 为完整状态向量"""
        return torch.cat([self.q, self.p])

    def clone(self, **overrides) -> 'EntityState':
        """深拷贝，支持部分字段覆盖"""
        ...
```

**实现要点**：
- `belief_cov` 必须保证正定：初始化时使用 `torch.eye(dim) * initial_variance`
- `attributes` 中的数值参数在加载时转为 Tensor（便于自动微分）
- `clone()` 用于仿真步进中创建新状态（避免原地修改）

### 1.2 CausalEdge

**文件**: `src/entities.py`

```python
@dataclass
class CausalEdge:
    source_id: int
    target_id: int
    mechanism: 'MechanismFunction'
    mechanism_type: str
    strength: float                    # α_ij ∈ [0, 1]
    delay: float                       # τ_ij（秒）
    confidence: float                  # ∈ [0, 1]

    def is_active(self, state: WorldState, threshold: float = 0.1) -> bool:
        """因果路由判断：该边在当前状态下是否激活"""
        # 路由分数 = strength × |Δs_source| × uncertainty_target × relevance
        ...
```

### 1.3 WorldState

**文件**: `src/entities.py`

```python
@dataclass
class WorldState:
    timestamp: float
    entities: Dict[int, EntityState]
    edges: List[CausalEdge]
    hamiltonian_value: float = None    # 当前总能量

    def get_entity(self, entity_id: int) -> EntityState:
        ...

    def entity_ids(self) -> List[int]:
        return list(self.entities.keys())

    def to_snapshot(self) -> dict:
        """序列化为 JSON 快照（兼容 data-format-spec.md）"""
        ...
    
    @classmethod
    def from_snapshot(cls, data: dict) -> 'WorldState':
        """从 JSON 快照反序列化"""
        ...
```

---

## 二、机制函数

### 2.1 MechanismFunction 基类

**文件**: `src/mechanisms/base.py`

```python
class MechanismFunction(nn.Module):
    """因果机制函数抽象基类。
    
    继承 nn.Module 以支持参数化（PINN）和自动微分。
    """
    
    def __init__(self, mechanism_type: str):
        super().__init__()
        self.mechanism_type = mechanism_type
    
    def delta_q(self, s_src: EntityState, s_tgt: EntityState) -> torch.Tensor:
        """对 target 广义坐标 q 的影响量"""
        return torch.zeros_like(s_tgt.q)
    
    def delta_p(self, s_src: EntityState, s_tgt: EntityState) -> torch.Tensor:
        """对 target 共轭动量 p 的影响量"""
        return torch.zeros_like(s_tgt.p)
    
    def forward(self, s_src: EntityState, s_tgt: EntityState) -> Tuple[torch.Tensor, torch.Tensor]:
        """完整前向：返回 (delta_q, delta_p)"""
        return self.delta_q(s_src, s_tgt), self.delta_p(s_src, s_tgt)
    
    def force_on(self, state: WorldState, target_id: int) -> torch.Tensor:
        """计算作用在 target_id 上的总广义力 F = -∂V/∂q"""
        f_total = torch.zeros_like(state.get_entity(target_id).q)
        for edge in state.edges:
            if edge.target_id == target_id:
                src = state.get_entity(edge.source_id)
                tgt = state.get_entity(edge.target_id)
                dq, dp = edge.mechanism(src, tgt)
                f_total += dq  # q 方向的力
        return f_total
```

### 2.2 ThermalConduction（热传导）

**文件**: `src/mechanisms/thermal.py`

```python
class ThermalConduction(MechanismFunction):
    """傅里叶定律：Q = k·A/d · (T_src - T_tgt)"""
    
    def __init__(self, conductivity: float, area: float, distance: float):
        super().__init__("thermal_conduction")
        self.k = torch.tensor(conductivity, dtype=torch.float64)
        self.A = torch.tensor(area, dtype=torch.float64)
        self.d = torch.tensor(distance, dtype=torch.float64)
        self.eff = self.k * self.A / self.d  # 有效传热系数
    
    def delta_p(self, s_src: EntityState, s_tgt: EntityState) -> torch.Tensor:
        """热流变化：J = kA/d · (T_src - T_tgt)"""
        dT = s_src.q[0] - s_tgt.q[0]  # q[0] = 温度
        heat_flux = self.eff * dT       # W
        return torch.tensor([heat_flux])
    
    def delta_q(self, s_src: EntityState, s_tgt: EntityState) -> torch.Tensor:
        """温度变化：dT = J·dt / (m·C)"""
        # 注意：delta_q 这里返回的是 dT/dt 的系数
        # 实际的 ΔT = delta_q · dt
        heat_flux = self.delta_p(s_src, s_tgt)
        C_total = s_tgt.attributes['mass'] * s_tgt.attributes['specific_heat']
        dT_dt = heat_flux / C_total
        return dT_dt
```

**实现要点**：
- `q[0]` 始终是温度（热力学实体的第一个广义坐标）
- `p[0]` 始终是热流（热力学实体的第一个共轭动量）
- 能量守恒：source 失去的热量 = target 获得的热量

### 2.3 SpringForce（弹簧力）

**文件**: `src/mechanisms/mechanical.py`

```python
class SpringForce(MechanismFunction):
    """胡克定律：F = -k·(x_tgt - x_src - L₀)"""
    
    def __init__(self, stiffness: float, rest_length: float = 0.0):
        super().__init__("spring_force")
        self.k = torch.tensor(stiffness, dtype=torch.float64)
        self.L0 = torch.tensor(rest_length, dtype=torch.float64)
    
    def delta_p(self, s_src: EntityState, s_tgt: EntityState) -> torch.Tensor:
        """弹簧力：F = -k·Δx（作用在 target 上）"""
        delta_x = s_tgt.q[0] - s_src.q[0] - self.L0
        force = -self.k * delta_x
        return torch.tensor([force])
    
    def delta_q(self, s_src: EntityState, s_tgt: EntityState) -> torch.Tensor:
        """速度变化：dv/dt = F/m"""
        force = self.delta_p(s_src, s_tgt)
        m = s_tgt.attributes['mass']
        return force / m
```

### 2.4 PINNMechanism（数据驱动）

**文件**: `src/mechanisms/pinn.py`

```python
class PINNMechanism(MechanismFunction):
    """PINN 参数化的通用因果机制函数。
    
    当物理定律不明确或需要从数据中学习时使用。
    网络输入：concat(s_src.full_state, s_tgt.full_state)
    网络输出：(delta_q, delta_p)
    """
    
    def __init__(self, state_dim: int, hidden_dims: List[int] = [64, 64, 32]):
        super().__init__("pinn_learned")
        in_dim = state_dim * 2  # source + target
        out_dim = state_dim     # delta_q + delta_p
        
        layers = []
        prev_dim = in_dim
        for h_dim in hidden_dims:
            layers.extend([nn.Linear(prev_dim, h_dim), nn.Tanh()])
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, out_dim))
        self.net = nn.Sequential(*layers)
        
        # 初始化：接近零输出（不破坏已有物理行为）
        for layer in self.net:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight, gain=0.01)
                nn.init.zeros_(layer.bias)
    
    def forward(self, s_src: EntityState, s_tgt: EntityState) -> Tuple[torch.Tensor, torch.Tensor]:
        x = torch.cat([s_src.full_state(), s_tgt.full_state()])
        out = self.net(x)
        dim_q = s_tgt.q.shape[0]
        return out[:dim_q], out[dim_q:]
```

**实现要点**：
- 初始化增益设为 0.01（小输出），避免 PINN 初期破坏已有因果结构
- 物理约束通过 loss 函数注入（非硬约束）
- 支持 partial mechanism：部分边用物理公式，部分用 PINN

---

## 三、辛积分器

**文件**: `src/integrator.py`

### 3.1 StörmerVerletIntegrator

```python
class StörmerVerletIntegrator:
    """速度 Verlet 辛积分器。
    
    算法：
      p_{1/2} = p_t + (dt/2) · F(q_t)
      q_{t+1} = q_t + dt · M^{-1} · p_{1/2}
      F_{t+1} = compute_forces(q_{t+1})
      p_{t+1} = p_{1/2} + (dt/2) · F_{t+1}
    
    性质：辛性、时间可逆、二阶精度 O(dt²)
    """
    
    def __init__(self, force_fn: Callable[[WorldState, int], torch.Tensor]):
        """
        Args:
            force_fn: force_fn(state, entity_id) → 广义力 F
        """
        self.force_fn = force_fn
    
    def step(self, state: WorldState, dt: float) -> WorldState:
        """执行一步 Verlet 积分。返回新 WorldState。"""
        new_entities = {}
        for eid, entity in state.entities.items():
            m = entity.attributes.get('mass', torch.tensor(1.0))
            F = self.force_fn(state, eid)
            
            # 半步动量
            p_half = entity.p + 0.5 * dt * F
            # 全步位置
            q_new = entity.q + dt * p_half / m
            
            # 创建临时状态计算新力
            temp_entity = entity.clone(q=q_new, p=p_half)
            temp_state = state.clone_with_entity(eid, temp_entity)
            F_new = self.force_fn(temp_state, eid)
            
            # 半步动量
            p_new = p_half + 0.5 * dt * F_new
            
            new_entities[eid] = entity.clone(q=q_new, p=p_new)
        
        return state.clone_with_entities(new_entities, timestamp=state.timestamp + dt)
```

### 3.2 Yoshida4Integrator

```python
class Yoshida4Integrator:
    """Yoshida 四阶辛积分器。
    
    S_4(dt) = S_2(x₁·dt) · S_2(x₀·dt) · S_2(x₁·dt)
    x₀ = 1 - 2·x₁, x₁ = 1/(2 - 2^{1/3}) ≈ 1.3512
    
    性质：辛性、时间可逆、四阶精度 O(dt⁴)
    """
    
    X1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))  # ≈ 1.3512
    X0 = 1.0 - 2.0 * X1                      # ≈ -1.7024
    
    def __init__(self, force_fn: Callable):
        self.force_fn = force_fn
        self.verlet = StörmerVerletIntegrator(force_fn)
    
    def step(self, state: WorldState, dt: float) -> WorldState:
        """三段 Verlet 组合。"""
        state = self.verlet.step(state, self.X1 * dt)
        state = self.verlet.step(state, self.X0 * dt)
        state = self.verlet.step(state, self.X1 * dt)
        return state
```

---

## 四、哈密顿投影

**文件**: `src/hamiltonian.py`

```python
class HamiltonianProjector:
    """将状态投影到能量守恒流形上。
    
    方法：拉格朗日乘子法
    目标：min ‖(q',p') - (q,p)‖²  s.t. H(q',p') = E_target
    """
    
    def __init__(self, energy_fn: Callable[[WorldState], float],
                 tolerance: float = 1e-6):
        """
        Args:
            energy_fn: energy_fn(state) → 系统总能量
            tolerance: 能量偏差容忍度
        """
        self.energy_fn = energy_fn
        self.E_target = None  # 在首次调用时设定
        self.tolerance = tolerance
    
    def initialize(self, initial_state: WorldState):
        """设定目标能量为初始状态的总能量"""
        self.E_target = self.energy_fn(initial_state)
    
    def project(self, state: WorldState) -> WorldState:
        """投影到能量流形。
        
        通过梯度下降法迭代修正：
          q' = q - λ · ∂H/∂q
          p' = p - λ · ∂H/∂p
        直到 |H(q',p') - E_target| < tolerance
        """
        if self.E_target is None:
            self.initialize(state)
        
        # 数值梯度
        E_current = self.energy_fn(state)
        if abs(E_current - self.E_target) < self.tolerance:
            return state  # 已满足约束
        
        # 简单投影：按动能/势能比例缩放
        # （完整实现需要自动微分计算 ∂H/∂q 和 ∂H/∂p）
        error = E_current - self.E_target
        scale = 1.0 - error / (2.0 * E_current + 1e-10)
        
        new_entities = {}
        for eid, entity in state.entities.items():
            # 对 p 进行缩放（动能 ∝ p²）
            new_entities[eid] = entity.clone(
                q=entity.q * (2.0 - scale),  # 互补缩放
                p=entity.p * scale
            )
        
        return state.clone_with_entities(new_entities)
```

**实现要点**：
- 投影应该在辛积分之后执行（管线 Step C）
- 投影不应过大：如果单步投影修正 > 1% 总能量，说明积分器步长过大
- 生产级实现应使用自动微分（`torch.autograd.grad`）而非数值梯度

---

## 五、CDABlock 完整管线

**文件**: `src/cdablock.py`

```python
class CDABlock:
    """CDA 核心计算块。
    
    管线：路由 → 机制计算 → 辛积分 → 哈密顿投影 → 贝叶斯更新
    """
    
    def __init__(self, integrator: 'SymplecticIntegrator',
                 projector: 'HamiltonianProjector',
                 bayesian_updater: Optional['BayesianUpdater'] = None):
        self.integrator = integrator
        self.projector = projector
        self.bayesian_updater = bayesian_updater
    
    def compute_forces(self, state: WorldState, entity_id: int) -> torch.Tensor:
        """汇总所有因果边对该实体的力"""
        force = torch.zeros_like(state.get_entity(entity_id).p)
        for edge in state.edges:
            if edge.target_id == entity_id and edge.is_active(state):
                src = state.get_entity(edge.source_id)
                tgt = state.get_entity(edge.target_id)
                _, dp = edge.mechanism(src, tgt)
                force += dp
        return force
    
    def step(self, state: WorldState, dt: float) -> WorldState:
        """一步完整的因果动力学步进"""
        # Step 1: 因果路由 + 力计算（在 compute_forces 中隐式完成）
        # Step 2: 辛积分（更新 q, p）
        self.integrator.force_fn = self.compute_forces
        new_state = self.integrator.step(state, dt)
        # Step 3: 哈密顿投影
        new_state = self.projector.project(new_state)
        # Step 4: 贝叶斯更新（可选）
        if self.bayesian_updater is not None:
            new_state = self.bayesian_updater.update(new_state)
        return new_state
    
    def simulate(self, initial_state: WorldState,
                 dt: float, n_steps: int,
                 observer: Optional[Callable] = None) -> List[WorldState]:
        """运行完整仿真，返回轨迹"""
        self.projector.initialize(initial_state)
        trajectory = [initial_state]
        state = initial_state
        
        for i in range(n_steps):
            state = self.step(state, dt)
            trajectory.append(state)
            if observer is not None:
                observer(state, i)
        
        return trajectory
```

---

## 六、学习组件

### 6.1 BayesianUpdater（EKF 贝叶斯更新）

**文件**: `src/learning/bayesian_update.py`

```python
class BayesianUpdater:
    """扩展卡尔曼滤波（EKF）贝叶斯状态更新。
    
    对应 CDA §6.2 Level 1。
    """
    
    def __init__(self, process_noise: float = 1e-4, 
                 observation_noise: float = 1e-2):
        self.Q = process_noise   # 过程噪声
        self.R = observation_noise  # 观测噪声
    
    def predict(self, entity: EntityState, dt: float) -> EntityState:
        """预测步：不确定性随时间增长"""
        dim = entity.state_dim
        # 状态不变，协方差增大
        new_cov = entity.belief_cov + self.Q * torch.eye(dim) * dt
        return entity.clone(belief_cov=new_cov)
    
    def update(self, entity: EntityState, 
               observation: torch.Tensor) -> EntityState:
        """更新步：用观测修正信念"""
        # K = P·H^T / (H·P·H^T + R)
        P = entity.belief_cov
        H = torch.eye(entity.state_dim)  # 观测矩阵（直接观测状态）
        S = H @ P @ H.T + self.R * torch.eye(entity.state_dim)
        K = P @ H.T @ torch.inverse(S)
        
        innovation = observation - entity.belief_mean
        new_mean = entity.belief_mean + K @ innovation
        new_cov = (torch.eye(entity.state_dim) - K @ H) @ P
        
        return entity.clone(belief_mean=new_mean, belief_cov=new_cov)
```

### 6.2 NOTEARS 因果发现

**文件**: `src/learning/notears.py`

```python
class NOTEARSDiscovery:
    """NOTEARS 因果结构学习。
    
    对应 CDA §6.1.2（骨架引导版本）。
    
    输入：时序观测矩阵 X ∈ R^{T×N}
    输出：邻接矩阵 W ∈ R^{N×N}（DAG）
    """
    
    def __init__(self, skeleton: Optional[np.ndarray] = None,
                 lambda1: float = 0.01, max_iter: int = 100):
        self.skeleton = skeleton      # 先验骨架 (N, N)
        self.lambda1 = lambda1        # L1 正则化系数
        self.max_iter = max_iter
    
    def discover(self, X: np.ndarray) -> np.ndarray:
        """从观测数据学习因果结构。
        
        Args:
            X: (T, N) 时序观测矩阵
            
        Returns:
            W: (N, N) 邻接矩阵，W[i,j] > 0 表示 i → j 的因果边
        """
        T, N = X.shape
        W = np.zeros((N, N))
        # 初始化：骨架边给予较大初始值
        if self.skeleton is not None:
            W = self.skeleton.copy()
        
        # 增广拉格朗日法求解
        # ...（完整实现见 CDA §6.1.2 参考代码）
        return W
```

---

## 七、数据加载器

**文件**: `src/data_loader.py`

```python
def load_graph(path: str) -> Tuple[Dict[int, EntityState], List[CausalEdge]]:
    """从 .graph.json 加载因果图。
    
    Returns:
        entities: {id: EntityState}
        edges: List[CausalEdge]
    """
    with open(path) as f:
        data = json.load(f)
    
    entities = {}
    for e_data in data['entities']:
        entity = EntityState(
            id=e_data['id'],
            name=e_data['name'],
            type=e_data['type'],
            domain=e_data['domain'],
            q=torch.tensor(e_data['position']['values'], dtype=torch.float64),
            p=torch.tensor(e_data['momentum']['values'], dtype=torch.float64),
            attributes=_convert_attrs(e_data['attributes']),
            belief_mean=torch.tensor(e_data['belief']['mean'], dtype=torch.float64),
            belief_cov=torch.tensor(e_data['belief']['covariance'], dtype=torch.float64),
        )
        entities[entity.id] = entity
    
    edges = []
    for e_data in data['edges']:
        mechanism = _create_mechanism(e_data)
        edge = CausalEdge(
            source_id=e_data['source_id'],
            target_id=e_data['target_id'],
            mechanism=mechanism,
            mechanism_type=e_data['mechanism_type'],
            strength=e_data['strength'],
            delay=e_data['delay'],
            confidence=e_data['confidence'],
        )
        edges.append(edge)
    
    return entities, edges


def load_trajectory(path: str) -> List[WorldState]:
    """从 .trajectory.json 加载轨迹。"""
    with open(path) as f:
        data = json.load(f)
    
    trajectory = []
    for snap in data['snapshots']:
        state = WorldState.from_snapshot(snap)
        trajectory.append(state)
    
    return trajectory


def _create_mechanism(edge_data: dict) -> MechanismFunction:
    """根据 edge 的 mechanism_type 和 function_form 创建对应的机制函数。
    
    分发逻辑（对应 data-format-spec §4.2 机制类型注册表）：
    
    Phase 1（确定性物理公式）：
      thermal_conduction + fourier_law → ThermalConduction
      thermal_conduction + radiation    → ThermalRadiation
      thermal_convection                  → ThermalConvection
      spring_force + hooke_law           → SpringForce
      damping_force                       → DampingForce
      pinn_learned                        → PINNMechanism
    
    Phase 2（可学习参数化，fallback）：
      * → CausalMechanismFunction（通用 W_type·Φ·σ 框架）
    """
    m_type = edge_data['mechanism_type']
    params = edge_data.get('mechanism_params', {})
    form = params.get('function_form', '')

    from src.mechanisms.thermal import ThermalConduction, ThermalConvection
    from src.mechanisms.mechanical import SpringForce, DampingForce
    from src.mechanisms.pinn import PINNMechanism

    if m_type == 'thermal_conduction' and form == 'fourier_law':
        return ThermalConduction(
            conductivity=params['conductivity'],
            area=params['cross_section_area'],
            distance=params['distance'],
        )
    elif m_type == 'thermal_conduction' and form == 'radiation':
        from src.mechanisms.thermal import ThermalRadiation
        return ThermalRadiation(
            emissivity=params.get('emissivity', 0.9),
            area=params.get('cross_section_area', 1.0),
        )
    elif m_type == 'thermal_convection':
        return ThermalConvection(
            h_conv=params.get('h_convection', 10.0),
            area=params.get('area', 1.0),
        )
    elif m_type == 'spring_force' and form == 'hooke_law':
        return SpringForce(
            stiffness=params['stiffness'],
            rest_length=params.get('rest_length', 0.0),
        )
    elif m_type == 'damping_force':
        return DampingForce(
            damping_coeff=params.get('damping_coeff', 1.0),
        )
    elif m_type == 'pinn_learned':
        pinn_cfg = params.get('pinn_params', {})
        return PINNMechanism(
            state_dim=pinn_cfg.get('input_dim', 6),
            hidden_dims=pinn_cfg.get('network_arch', [64, 64, 32]),
        )
    else:
        from src.mechanisms.causal_mechanism import CausalMechanismFunction
        return CausalMechanismFunction(
            causal_type=m_type,
            state_dim=params.get('state_dim', 6),
        )
```

---

## 八、Phase 2：通用机制函数框架（CDA §3.3）

> **Phase 分层说明**：§二~§七中的机制函数为 Phase 1 实现（确定性物理公式，直接计算）。
> §八~§九为 Phase 2 框架规格（可学习参数化，从 CDA §3.3 完整迁移）。
> 两层通过 `PhysicsPlusResidualPINN`（见 pinn-templates.md §六）桥接。

### 8.1 MechanismTypeRegistry（机制类型约束注册表）

**文件**: `src/mechanisms/registry.py`

对应 CDA §3.3.1。每种因果类型定义 W 矩阵的结构约束，保证梯度下降不可能违反物理定律。

```python
class MechanismTypeRegistry:
    """因果机制类型注册表。
    
    约束在参数化层面保证，而非损失函数层面。
    无论梯度如何更新，W_type 始终满足物理定律。
    """

    @staticmethod
    def mechanical_W(raw_A: torch.Tensor) -> torch.Tensor:
        """力学型：牛顿第三定律（作用力 = 反作用力）。
        W = A - A^T → W^T = -W（反对称）。
        自由度：d(d-1)/2。
        """
        return raw_A - raw_A.T

    @staticmethod
    def thermal_W(raw_A: torch.Tensor, beta: float = 5.0) -> torch.Tensor:
        """热力学型：热力学第二定律（热量从高温流向低温）。
        W = exp(-β·sigmoid(A))，所有元素 ∈ (0,1]，保证热流方向正确。
        """
        return torch.exp(-beta * torch.sigmoid(raw_A))

    @staticmethod
    def information_W(raw_diag: torch.Tensor, gamma: float = 1.0) -> torch.Tensor:
        """信息型：信号衰减（强度随距离递减）。
        W = diag(exp(-γ·|a_i|))，对角衰减矩阵。
        """
        return torch.diag(torch.exp(-gamma * torch.abs(raw_diag)))

    @staticmethod
    def chemical_W(raw_A: torch.Tensor) -> torch.Tensor:
        """化学型：质量守恒（所有反应物的质量转移总和为零）。
        W 行和为零（流入 = 流出）。
        W = A - diag(A·1)。
        """
        row_sum = raw_A.sum(dim=1, keepdim=True)
        return raw_A - row_sum / raw_A.shape[1]
```

### 8.2 InteractionBasis（状态交互基函数 Φ）

**文件**: `src/mechanisms/interaction_basis.py`

对应 CDA §3.3.2。可学习部分，捕获"实体 i 在实体 j 影响下的状态变化"。

```python
class InteractionBasis(nn.Module):
    """状态交互基函数 Φ(s_i, s_j)。
    
    设计原则：
    - 分离变量：Φ = Σ_k φ_k(s_i) · ψ_k(s_j)
    - 物理量纲一致性：每个基函数对应一个物理量纲通道
    - 多尺度交互：低阶捕获线性效应，高阶捕获非线性耦合
    """

    def __init__(self, state_dim: int, hidden_dim: int = 64, num_basis: int = 16):
        super().__init__()
        self.state_dim = state_dim
        self.num_basis = num_basis

        self.source_encoder = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, num_basis),
        )
        self.target_encoder = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, num_basis),
        )
        self.basis_weights = nn.Parameter(torch.randn(num_basis, state_dim) * 0.01)

    def forward(self, s_i: torch.Tensor, s_j: torch.Tensor) -> torch.Tensor:
        """计算 Φ(s_i, s_j) ∈ R^state_dim。
        
        Args:
            s_i: 目标实体状态 (batch, state_dim)
            s_j: 源实体状态 (batch, state_dim)
        Returns:
            delta_s: 状态变化量 (batch, state_dim)
        """
        h_i = self.target_encoder(s_i)
        h_j = self.source_encoder(s_j)
        interaction = h_i * h_j
        return interaction @ self.basis_weights
```

### 8.3 CausalDecay（因果强度衰减 σ）

**文件**: `src/mechanisms/decay.py`

对应 CDA §3.3.3。

```python
class CausalDecay(nn.Module):
    """因果强度衰减函数。
    
    σ(r) = exp(-α·r)              指数衰减（默认，中程如热传导）
    σ(r) = 1/(1+α·r²)             逆二次衰减（长程如引力）
    σ(r) = exp(-(α·r)²)           高斯衰减（短程如化学反应）
    
    衰减类型由因果类型自动决定（DECAY_RULES）。
    """

    DECAY_RULES = {
        'mechanical': 'inverse_quadratic',
        'thermal':    'exponential',
        'chemical':   'gaussian',
        'information':'exponential',
    }

    def __init__(self, causal_type: str):
        super().__init__()
        self.decay_type = self.DECAY_RULES.get(causal_type, 'exponential')
        self.alpha = nn.Parameter(torch.tensor(1.0))

    def forward(self, distance: torch.Tensor) -> torch.Tensor:
        r = distance + 1e-8
        if self.decay_type == 'exponential':
            return torch.exp(-self.alpha * r)
        elif self.decay_type == 'inverse_quadratic':
            return 1.0 / (1.0 + self.alpha * r ** 2)
        elif self.decay_type == 'gaussian':
            return torch.exp(-(self.alpha * r) ** 2)
```

### 8.4 CausalMechanismFunction（完整参数化组装）

**文件**: `src/mechanisms/causal_mechanism.py`

对应 CDA §3.3.4。`f_ij = W_type · Φ(s_i, s_j) · σ(α·distance)`

```python
class CausalMechanismFunction(nn.Module):
    """因果机制函数 f_ij(s_i, s_j; θ) 的完整实现。
    
    f_ij = strength · (Φ(s_i, s_j) · W_type^T) · σ(distance)
    
    这是 CDA 的通用机制函数框架，Phase 1 的确定性物理公式是其特例。
    """

    def __init__(self, causal_type: str, state_dim: int,
                 hidden_dim: int = 64, num_basis: int = 16):
        super().__init__()
        self.causal_type = causal_type
        raw_dim = state_dim
        self.raw_W = nn.Parameter(torch.randn(raw_dim, raw_dim) * 0.01)
        self.phi = InteractionBasis(state_dim, hidden_dim, num_basis)
        self.decay = CausalDecay(causal_type)
        self.strength = nn.Parameter(torch.tensor(0.5))
        self.registry = MechanismTypeRegistry()

    def get_W(self) -> torch.Tensor:
        """获取受物理约束的 W_type 矩阵"""
        if self.causal_type == 'mechanical':
            return self.registry.mechanical_W(self.raw_W)
        elif self.causal_type == 'thermal':
            return self.registry.thermal_W(self.raw_W)
        elif self.causal_type == 'information':
            diag = F.softplus(self.raw_W.diagonal())
            return self.registry.information_W(diag)
        elif self.causal_type == 'chemical':
            return self.registry.chemical_W(self.raw_W)
        else:
            return self.raw_W

    def forward(self, s_i: torch.Tensor, s_j: torch.Tensor,
                distance: torch.Tensor) -> torch.Tensor:
        """计算实体 i 在实体 j 影响下的状态变化 Δs_i。
        
        Args:
            s_i: 目标实体状态 (batch, state_dim)
            s_j: 源实体状态 (batch, state_dim)
            distance: 因果距离 (batch, 1)
        Returns:
            delta_s: 状态变化量 (batch, state_dim)
        """
        W = self.get_W()
        phi_val = self.phi(s_i, s_j)
        decay_val = self.decay(distance)
        strength = torch.sigmoid(self.strength)
        return strength * (phi_val @ W.T) * decay_val
```

---

## 九、Phase 2：因果计算路由（CDA §3.4）

> **Phase 分层说明**：Phase 1 的 CDABlock 使用简单 `edge.is_active()` 判断。
> Phase 2 引入完整 CausalRouter，支持 N > 1000 实体的大规模系统。

**文件**: `src/routing/causal_router.py`

对应 CDA §3.4。物理语义驱动的稀疏边选择。

```python
class CausalRouter:
    """因果计算路由器。
    
    路由分数 r_ij = α_ij × S_change(i) × S_unc(j) × Q(j)
    
    - α_ij: 因果强度（边的固有属性）
    - S_change(i): 源实体最近的状态变化显著性（tanh 归一化）
    - S_unc(j): 目标实体的当前不确定性（sigmoid 归一化）
    - Q(j): 查询相关性（可选，无查询时恒为 1）
    
    三级筛选策略：
      Level 1: 硬阈值（分数 < 0.01 的边直接跳过）
      Level 2: Top-K（每个目标实体保留分数最高的 k 条入边）
      Level 3: 全局预算（总边数不超过 max_edges）
    
    复杂度：O(N²k) → O(NKk)，K ≪ N 时 640× 加速。
    """

    def __init__(self, num_entities: int, top_k: int = 16,
                 max_edges: int = 2048, hard_threshold: float = 0.01):
        self.num_entities = num_entities
        self.top_k = top_k
        self.max_edges = max_edges
        self.hard_threshold = hard_threshold

    def route(self, world: WorldState,
              query_entities: Optional[Set[int]] = None) -> Set[Tuple[int, int]]:
        """计算本步需要激活的因果边集合。
        
        Args:
            world: 当前世界状态
            query_entities: 查询关注的实体集合（可选）
            
        Returns:
            active_edges: Set[(source_id, target_id)] 本步需要计算的边
        """
        scores = self._compute_scores(world, query_entities)

        # Level 1: 硬阈值过滤
        mask = scores > self.hard_threshold

        # Level 2: 每个目标实体保留 top-k 入边
        selected = torch.zeros_like(mask)
        for j in range(self.num_entities):
            col = scores[:, j] * mask[:, j]
            nonzero = (col > 0).sum().item()
            k = min(self.top_k, nonzero)
            if k > 0:
                top_idx = col.topk(k).indices
                selected[top_idx, j] = True

        # Level 3: 全局预算上限
        total = selected.sum().item()
        if total > self.max_edges:
            flat = (scores * selected).flatten()
            cutoff = flat.topk(self.max_edges).values[-1]
            selected &= (scores >= cutoff)

        # 转换为边集合
        active = set()
        idx = selected.nonzero()
        for row in idx:
            active.add((row[0].item(), row[1].item()))
        return active

    def _compute_scores(self, world: WorldState,
                        query_entities: Optional[Set[int]]) -> torch.Tensor:
        """计算 N×N 路由分数矩阵"""
        scores = torch.zeros(self.num_entities, self.num_entities)

        for edge in world.edges:
            i, j = edge.source_id, edge.target_id

            alpha = edge.strength

            # 源实体状态变化显著性
            delta = self._recent_state_change(world, i)
            s_change = torch.tanh(delta / (self._state_scale(world, i) + 1e-8))

            # 目标实体不确定性
            sigma_trace = world.get_entity(j).belief_cov.trace().item()
            s_unc = torch.sigmoid((sigma_trace - self._unc_thresh) / self._unc_scale)

            # 查询相关性
            q_rel = 1.0
            if query_entities is not None:
                q_rel = float(j in query_entities)

            scores[i, j] = alpha * (1.0 + s_change) * (1.0 + s_unc) * q_rel

        return scores

    @staticmethod
    def _recent_state_change(world: WorldState, entity_id: int) -> float:
        """获取实体最近的状态变化量（需要 WorldState 保存历史快照）"""
        # Phase 1 简化：返回 q 的绝对值作为代理
        return world.get_entity(entity_id).q.abs().sum().item()

    @staticmethod
    def _state_scale(world: WorldState, entity_id: int) -> float:
        return world.get_entity(entity_id).q.abs().mean().item() + 1e-8

    _unc_thresh: float = 0.1
    _unc_scale: float = 1.0
```

### 9.1 CDABlock 路由集成

Phase 2 的 CDABlock 应集成 CausalRouter，替代简单的 `edge.is_active()` 判断：

```python
class CDABlockV2(CDABlock):
    """Phase 2 CDABlock：集成因果路由器。
    
    与 Phase 1 的区别：
    - Step 1 前增加路由决策（CausalRouter.route）
    - 仅对 active_edges 计算机制函数
    - 支持大规模实体系统（N > 1000）
    """

    def __init__(self, integrator, projector, router: CausalRouter,
                 bayesian_updater=None):
        super().__init__(integrator, projector, bayesian_updater)
        self.router = router

    def compute_forces(self, state: WorldState, entity_id: int) -> torch.Tensor:
        """汇总路由选中边对该实体的力"""
        force = torch.zeros_like(state.get_entity(entity_id).p)
        for edge in state.edges:
            if (edge.source_id, edge.target_id) in self._active_edges:
                if edge.target_id == entity_id:
                    src = state.get_entity(edge.source_id)
                    tgt = state.get_entity(edge.target_id)
                    _, dp = edge.mechanism(src, tgt)
                    force += dp
        return force

    def step(self, state: WorldState, dt: float) -> WorldState:
        """带路由的因果动力学步进"""
        # Step 0: 路由决策
        self._active_edges = self.router.route(state)
        # Step 1~4: 同 Phase 1
        self.integrator.force_fn = self.compute_forces
        new_state = self.integrator.step(state, dt)
        new_state = self.projector.project(new_state)
        if self.bayesian_updater is not None:
            new_state = self.bayesian_updater.update(new_state)
        return new_state
```
