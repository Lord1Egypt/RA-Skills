# CDA 数据格式规范（Data Format Specification）

> **版本**: v0.1.0
> **状态**: 初版提案
> **所有权**: CDA Data Synthesizer 技能
> 
> **本文件为 `cda-data-synth` 技能权威副本，供 Code Lab 技能直接引用。**
> **更新时须同步两个技能中的此文件。**

本文件定义 Causal Dynamics Architecture 的核心数据序列化协议。所有 CDA 组件（仿真引擎、训练管线、评估框架）必须遵守此格式。

---

## 一、总体设计原则

1. **JSON-first**：以 JSON 为主要序列化格式，人类可读、工具链友好
2. **NumPy 兼容**：所有张量/矩阵字段设计为可直接 `np.array()` 加载
3. **float64 精度**：所有数值字段在加载时必须转为 `torch.float64` / `np.float64`。物理仿真对数值精度高度敏感，JSON 本身不区分 float32/float64，但 consuming 端（Code Lab）应始终以双精度处理。`belief.covariance` 尤其需要高精度以保证正定性
4. **因果图 = 拓扑 + 动力学**：静态结构（实体+边）和动态行为（机制函数参数）分离
5. **时间序列友好**：轨迹数据按 snapshot 组织，支持稀疏/密集采样

---

## 二、核心数据结构

### 2.1 EntityState（实体状态）

对应 CDA §3.1 的 `EntityState` 类。

```json
{
  "id": 0,
  "name": "compressor_1",
  "type": "thermal_node",
  "domain": "thermodynamics",
  "position": {
    "values": [350.0, 0.0, 0.0],
    "coordinates": ["temperature_K", "x_m", "y_m"],
    "units": ["K", "m", "m"]
  },
  "momentum": {
    "values": [1500.0, 0.0, 0.0],
    "coordinates": ["heat_flux_W", "velocity_x", "velocity_y"],
    "units": ["W", "m/s", "m/s"]
  },
  "attributes": {
    "mass": 25.0,
    "specific_heat": 500.0,
    "thermal_conductivity": 50.0,
    "volume": 0.05,
    "material_type": "steel"
  },
  "belief": {
    "distribution_type": "gaussian",
    "mean": [350.0, 0.0, 0.0],
    "covariance": [
      [1.0, 0.0, 0.0],
      [0.0, 0.01, 0.0],
      [0.0, 0.0, 0.01]
    ]
  }
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | int | ✅ | 实体唯一标识符（全局） |
| `name` | string | ✅ | 人类可读名称 |
| `type` | string | ✅ | 实体类型（见 §2.5 类型注册表） |
| `domain` | string | ✅ | 所属物理域（thermodynamics/mechanics/fluid/circuit） |
| `position` | object | ✅ | 广义坐标 q |
| `position.values` | float[] | ✅ | 坐标值数组 |
| `position.coordinates` | string[] | ✅ | 每个维度的物理含义 |
| `position.units` | string[] | ✅ | 每个维度的单位 |
| `momentum` | object | ✅ | 共轭动量 p（结构同 position） |
| `attributes` | object | ✅ | 固有属性（质量、材料参数等，域相关） |
| `belief` | object | ✅ | 贝叶斯信念分布 |

**belief 子结构**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `distribution_type` | string | 目前仅支持 `gaussian`，预留 `mixture`, `laplace` |
| `mean` | float[] | 信念均值（维度 = position + momentum） |
| `covariance` | float[][] | 协方差矩阵（方阵，维度同 mean） |

---

### 2.2 CausalEdge（因果边）

对应 CDA §3.1 的 `CausalEdge` 类。

```json
{
  "source_id": 0,
  "target_id": 1,
  "mechanism_type": "thermal_conduction",
  "mechanism_params": {
    "conductivity": 50.0,
    "cross_section_area": 0.01,
    "distance": 2.0,
    "function_form": "fourier_law"
  },
  "strength": 0.85,
  "delay": 0.0,
  "confidence": 0.95,
  "source_knowledge": "physics_equation"
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source_id` | int | ✅ | 因端实体 ID |
| `target_id` | int | ✅ | 果端实体 ID |
| `mechanism_type` | string | ✅ | 机制类型（见 §2.6 机制类型注册表） |
| `mechanism_params` | object | ✅ | 机制函数参数（域相关，见 §2.7） |
| `strength` | float | ✅ | 因果强度 α_ij ∈ [0, 1] |
| `delay` | float | ✅ | 传播延迟 τ_ij（秒），0 表示即时 |
| `confidence` | float | ✅ | 置信度 ∈ [0, 1] |
| `source_knowledge` | string | ✅ | 知识来源（physics_equation/topology_diagram/equipment_manual/expert/data_inferred） |

**自环边语义（source_id == target_id）**：

当 `source_id == target_id` 时，表示**外部干预或边界条件**作用在该实体自身，而非实体间的因果传播。典型场景：

| 场景 | mechanism_type | 语义 |
|------|---------------|------|
| 空调制冷 | `thermal_convection` | 外部冷源对房间的热注入/提取 |
| 散热器加热 | `thermal_convection` | 外部热源对房间的热注入 |
| 外力施加 | `spring_force` | 外部边界条件/载荷 |
| 控制器反馈 | `pinn_learned` | 自适应控制器对自身状态的修正 |

自环边的机制函数 `f(s_self, s_self)` 只接收一个实体的状态作为输入，输出该实体的状态变化量 Δs。在因果传播计算中，自环边应在普通因果边**之后**处理（先计算实体间传播，再叠加外部干预）。

---

### 2.3 WorldState（世界状态快照）

一个时刻的完整系统状态。

```json
{
  "timestamp": 0.0,
  "time_unit": "s",
  "entities": [
    { "..." : "EntityState 对象（同 §2.1）" }
  ],
  "edges": [
    { "..." : "CausalEdge 对象（同 §2.2）" }
  ],
  "hamiltonian": {
    "total_energy": 45000.0,
    "kinetic_energy": 0.0,
    "potential_energy": 45000.0,
    "energy_error": 1.2e-6,
    "conservation_violated": false
  }
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `timestamp` | float | 时刻值 |
| `time_unit` | string | 时间单位（s/min/h） |
| `entities` | EntityState[] | 当前时刻所有实体状态 |
| `edges` | CausalEdge[] | 当前时刻所有因果边（通常不变，但在线学习可变） |
| `hamiltonian` | object | 哈密顿量守恒检查（可选，用于验证） |

---

## 三、文件类型规范

### 3.1 Graph 文件（*.graph.json）

静态因果图定义。包含初始时刻的完整系统状态。

```json
{
  "version": "0.1.0",
  "format": "cda-graph",
  "metadata": {
    "name": "building_thermal_system",
    "domain": "thermodynamics",
    "description": "三房间建筑热力学系统",
    "entity_count": 5,
    "edge_count": 6,
    "created_by": "cda-data-synth",
    "creation_time": "2026-04-27T03:00:00Z"
  },
  "entities": [ "..." ],
  "edges": [ "..." ],
  "initial_state": {
    "timestamp": 0.0,
    "hamiltonian": {
      "initial_total_energy": 45000.0
    }
  },
  "hamiltonian_definition": {
    "type": "custom",
    "potential_function": {
      "type": "pairwise",
      "form": "V(q) = sum_{i<j} (alpha_ij * (q_i - q_j)^2)",
      "params": {
        "note": "alpha_ij stored in edge mechanism_params"
      }
    },
    "conservation_quantity": "total_energy",
    "tolerance": 1.0e-4
  }
}
```

### 3.2 Trajectory 文件（*.trajectory.json）

时序轨迹。由多个 WorldState 快照组成。

```json
{
  "version": "0.1.0",
  "format": "cda-trajectory",
  "metadata": {
    "graph_ref": "building_thermal_system.graph.json",
    "snapshot_count": 1000,
    "time_range": {
      "start": 0.0,
      "end": 3600.0,
      "unit": "s"
    },
    "sampling": {
      "method": "uniform",
      "dt": 3.6,
      "steps": 1000
    },
    "generator": {
      "method": "störmer-verlet",
      "noise_level": 0.01
    }
  },
  "snapshots": [
    {
      "timestamp": 0.0,
      "entities": [ "..." ],
      "hamiltonian": { "..." }
    },
    {
      "timestamp": 3.6,
      "entities": [ "..." ],
      "hamiltonian": { "..." }
    }
  ]
}
```

**优化建议**：对于大型轨迹（>100 实体 × >10000 时间步），考虑分片存储：
```
trajectory/
  ├── meta.json          （metadata）
  ├── snapshot_000.json   （t=0 ~ t=99）
  ├── snapshot_001.json   （t=100 ~ t=199）
  └── ...
```

### 3.3 Hamiltonian 文件（*.hamiltonian.json）

哈密顿量的完整定义。用于训练时的能量约束。

```json
{
  "version": "0.1.0",
  "format": "cda-hamiltonian",
  "metadata": {
    "domain": "thermodynamics",
    "entity_count": 5
  },
  "kinetic_energy": {
    "formula": "T(p) = sum_i (p_i^2 / (2 * C_i * m_i))",
    "parameters": {
      "C": [500.0, 500.0, 500.0, 500.0, 500.0],
      "m": [25.0, 25.0, 25.0, 25.0, 25.0]
    },
    "note": "C_i = specific_heat, p_i = heat_flux analogy"
  },
  "potential_energy": {
    "formula": "V(q) = sum_{edges} alpha_ij * k_ij * A_ij / d_ij * (T_i - T_j)^2 / 2",
    "parameters": {
      "note": "Edge-dependent, see mechanism_params in edges"
    },
    "note": "Thermal analogy: potential = stored thermal energy"
  },
  "total_energy": {
    "E_total": 45000.0,
    "tolerance": 1.0e-4,
    "enforcement": "hard_constraint"
  }
}
```

### 3.4 Meta 文件（*.meta.json）

数据集元信息，用于索引和管理。

```json
{
  "version": "0.1.0",
  "dataset_name": "thermal_building_3room",
  "description": "三房间建筑热力学仿真：室外→外墙→房间→内墙→房间，含空调和散热器",
  "files": {
    "graph": "thermal_building_3room.graph.json",
    "trajectory": "thermal_building_3room.trajectory.json",
    "hamiltonian": "thermal_building_3room.hamiltonian.json"
  },
  "statistics": {
    "entity_count": 5,
    "edge_count": 6,
    "trajectory_steps": 1000,
    "time_range_s": [0.0, 3600.0],
    "state_dimension": 6
  },
  "tags": ["thermodynamics", "building", "phase1", "multi-entity"]
}
```

---

## 四、类型注册表

### 4.1 实体类型（entity type）

| type | domain | 广义坐标 q | 共轭动量 p | 典型属性 |
|------|--------|-----------|-----------|---------|
| `thermal_node` | thermodynamics | 温度 T [K] | 热流 J [W] | mass, specific_heat, thermal_conductivity |
| `mechanical_body` | mechanics | 位移 x [m] | 动量 p [kg·m/s] | mass, stiffness, damping |
| `fluid_cell` | fluid | 压力 P [Pa] | 质量流 J_m [kg/s] | volume, viscosity, density |
| `circuit_node` | circuit | 电压 V [V] | 电流 I [A] | capacitance, resistance |
| `chemical_species` | chemistry | 浓度 c [mol/L] | 反应流 J_r [mol/s] | molecular_weight, activation_energy |
| `abstract_entity` | general | 任意 | 任意 | 无约束 |

### 4.2 机制类型（mechanism type）

| mechanism_type | 因果关系 | 公式 | 对应物理定律 |
|---------------|---------|------|-------------|
| `thermal_conduction` | T_hot → T_cold | Q = k·A·(T_i - T_j)/d | 傅里叶定律 |
| `thermal_convection` | T_surface → T_fluid | Q = h·A·(T_s - T_f) | 牛顿冷却定律 |
| `thermal_radiation` | T_body → T_absorber | Q = ε·σ·A·(T_i⁴ - T_j⁴) | Stefan-Boltzmann |
| `spring_force` | x_displacement → F | F = -k·(x_i - x_j) | 胡克定律 |
| `damping_force` | v_velocity → F | F = -c·v | 粘性阻尼 |
| `gravitational` | mass → mass | F = -G·m_i·m_j/r² | 万有引力 |
| `pressure_driven_flow` | P_high → P_low | Q = ΔP/R | 压力驱动流动 |
| `ohmic_resistance` | V → I | I = (V_i - V_j)/R | 欧姆定律 |
| `chemical_reaction` | c_reactant → c_product | J = k·c^n | 质量作用定律 |
| `pinn_learned` | general → general | f(q, p; θ) | 数据驱动 PINN |

---

## 五、机制参数格式（§2.7 详解）

不同 mechanism_type 的 `mechanism_params` 结构：

### 5.1 thermal_conduction

```json
{
  "conductivity": 50.0,
  "cross_section_area": 0.01,
  "distance": 2.0,
  "function_form": "fourier_law",
  "pinn_params": null
}
```

### 5.2 spring_force

```json
{
  "stiffness": 1000.0,
  "rest_length": 1.0,
  "damping_coeff": 5.0,
  "function_form": "hooke_law",
  "pinn_params": null
}
```

### 5.3 pinn_learned（数据驱动）

```json
{
  "function_form": "pinn",
  "pinn_params": {
    "network_arch": [64, 64, 32],
    "activation": "tanh",
    "trained": false,
    "param_count": 8000
  }
}
```

---

## 六、Python 加载接口

推荐的数据加载代码骨架（Code Lab 技能会基于此生成完整实现）：

```python
@dataclass
class EntityState:
    id: int
    name: str
    type: str
    domain: str
    position: np.ndarray      # (dim_q,)
    momentum: np.ndarray      # (dim_p,)
    attributes: dict
    belief_mean: np.ndarray   # (dim_q + dim_p,)
    belief_cov: np.ndarray    # (dim, dim)

@dataclass
class CausalEdge:
    source_id: int
    target_id: int
    mechanism_type: str
    mechanism_params: dict
    strength: float
    delay: float
    confidence: float

@dataclass
class WorldState:
    timestamp: float
    entities: Dict[int, EntityState]
    edges: List[CausalEdge]

def load_graph(path: str) -> Tuple[Dict[int, EntityState], List[CausalEdge]]:
    """从 .graph.json 加载静态因果图"""
    ...

def load_trajectory(path: str) -> List[WorldState]:
    """从 .trajectory.json 加载时序轨迹"""
    ...
```

---

## 七、版本策略

- **主版本号**（X.0.0）：破坏性格式变更，不兼容旧版
- **次版本号**（0.X.0）：新增可选字段，向后兼容
- **补丁号**（0.0.X）：文档修正、示例更新

当前版本 `0.1.0`：定义了热力学域的完整格式，力学和流体域的属性参数待补充。
