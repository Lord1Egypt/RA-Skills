# CDA 因果数据合成协议（Synthesis Protocols）

> **配合**: `data-format-spec.md` v0.1.0
> **作用**: 定义各物理域的实体拓扑设计、机制参数化、仿真参数选择、噪声注入策略

---

## 一、通用合成流程

```
输入：场景描述（自然语言）
  ↓
Step 1: 域识别（thermodynamics / mechanics / fluid / coupling）
  ↓
Step 2: 实体设计（类型、数量、初始状态、属性）
  ↓
Step 3: 因果拓扑设计（边：source→target、机制类型、参数）
  ↓
Step 4: 哈密顿量定义（势能函数、守恒量）
  ↓
Step 5: 前向仿真（积分器 + 机制函数 → 轨迹）
  ↓
Step 6: 观测噪声注入（模拟真实传感器）
  ↓
Step 7: 序列化输出（按 data-format-spec.md 格式）
```

---

## 二、热力学域合成协议

### 2.1 实体设计规则

**实体类型**: `thermal_node`

**广义坐标 q**: 温度 T（标量或向量）
**共轭动量 p**: 热流 J（标量，W）
**典型属性**:

| 属性 | 符号 | 单位 | 典型范围 | 设计方法 |
|------|------|------|---------|---------|
| 质量 | m | kg | 1 ~ 10000 | 根据对象体量设定 |
| 比热容 | C | J/(kg·K) | 100 ~ 2000 | 根据材料查表 |
| 导热系数 | k | W/(m·K) | 0.01 ~ 400 | 根据材料查表 |

**初始温度分布设计**:

| 场景 | 推荐分布 | 说明 |
|------|---------|------|
| 稳态分析 | 均匀温度 + 小扰动 | 验证收敛性 |
| 瞬态分析 | 线性梯度 | 验证热传导方向 |
| 阶跃响应 | 单点高温 + 低温环境 | 验证动态响应 |
| 自然演化 | 随机初始化 [280, 370]K | 验证长期行为 |

### 2.2 因果边设计规则

**机制类型**: `thermal_conduction`（主导）、`thermal_convection`（可选）、`thermal_radiation`（高温场景）

**傅里叶定律参数化**:

```
Q_ij = (k_eff * A_ij / d_ij) * (T_i - T_j)

其中：
  k_eff = 等效导热系数（串联/并联取调和/算术平均）
  A_ij = 传热面积
  d_ij = 传热距离

因果强度 α_ij = min(1, Q_ij / Q_max)
```

**典型因果拓扑**:

```
建筑场景：
  outdoor ──→ wall ──→ room_A ──→ inner_wall ──→ room_B
    │           │                          │            │
    └───────────┘                          └────────────┘
```

### 2.3 仿真参数

| 参数 | 推荐值 | 说明 |
|------|-------|------|
| 积分器 | Störmer-Verlet | 辛积分器，能量守恒 |
| dt | 0.1 ~ 10.0 s | 根据热时间常数选择（τ = mC/kA） |
| 总时长 | 3~5 个热时间常数 | 确保接近稳态 |
| 噪声模型 | Gaussian N(0, σ²) | σ = 0.1 ~ 1.0 K（温度），0.5 ~ 5.0 W（热流） |

### 2.4 哈密顿量定义

热力学类比：

```
动能（类比）：T(p) = sum_i p_i² / (2·C_i·m_i)
  这里 p_i 是热流类比量，C_i·m_i 是热容

势能（类比）：V(q) = sum_{edges} α_ij · k_ij · A_ij / d_ij · (T_i - T_j)² / 2

总能量：E = T + V = const（热平衡时所有温度相等，势能最小化）
```

---

## 三、力学域合成协议

### 3.1 实体设计规则

**实体类型**: `mechanical_body`

**广义坐标 q**: 位移 x（1D/2D/3D）
**共轭动量 p**: 动量 p = m·v
**典型属性**:

| 属性 | 符号 | 单位 | 典型范围 |
|------|------|------|---------|
| 质量 | m | kg | 0.01 ~ 1000 |
| 刚度 | k | N/m | 10 ~ 100000 |
| 阻尼系数 | c | N·s/m | 0.01 ~ 100 |

**初始条件设计**:

| 场景 | 推荐初始条件 |
|------|-------------|
| 自由振动 | 初始位移 + 零速度 |
| 受迫振动 | 零初始 + 周期性外力 |
| 碰撞 | 两物体相向运动 |

### 3.2 因果边设计规则

**机制类型**: `spring_force`（主导）、`damping_force`、`gravitational`

**胡克定律参数化**:

```
F_ij = -k_ij · (x_i - x_j - L_0) · n_ij

其中：
  k_ij = 弹簧刚度
  L_0 = 自然长度
  n_ij = 从 j 到 i 的单位方向向量

因果强度 α_ij = k_ij / k_max
```

### 3.3 仿真参数

| 参数 | 推荐值 |
|------|-------|
| 积分器 | Störmer-Verlet 或 Yoshida 4阶 |
| dt | 0.001 ~ 0.01 s |
| 总时长 | 10~50 个振动周期（T = 2π√(m/k)) |

### 3.4 哈密顿量定义

```
动能：T(p) = sum_i p_i² / (2·m_i)
势能：V(q) = sum_{edges} k_ij·(x_i - x_j - L_0)² / 2 + m_i·g·h_i
总能量：E = T + V = const
```

---

## 四、流体域合成协议

### 4.1 实体设计规则

**实体类型**: `fluid_cell`

**广义坐标 q**: 压力 P（Pa）
**共轭动量 p**: 质量流率 J_m（kg/s）
**典型属性**:

| 属性 | 符号 | 单位 | 典型范围 |
|------|------|------|---------|
| 体积 | V | m³ | 0.001 ~ 10 |
| 粘度 | μ | Pa·s | 0.001 ~ 1 |
| 密度 | ρ | kg/m³ | 0.5 ~ 1500 |

### 4.2 因果边设计规则

**机制类型**: `pressure_driven_flow`

**参数化**:

```
J_m = (P_i - P_j) / R_ij

其中 R_ij = 128·μ·L / (π·D⁴)（Hagen-Poiseuille）
```

### 4.3 仿真参数

| 参数 | 推荐值 |
|------|-------|
| 积分器 | Störmer-Verlet |
| dt | 0.01 ~ 1.0 s |
| 总时长 | 压力平衡时间常数 |

---

## 五、多域耦合合成协议

### 5.1 耦合方式

| 耦合对 | 耦合机制 | 因果边类型 |
|--------|---------|-----------|
| 热 ↔ 力 | 热膨胀/温度相关刚度 | `thermal_expansion` |
| 力 ↔ 流 | 压力驱动变形 | `pressure_deformation` |
| 热 ↔ 流 | 对流传热 | `thermal_convection` |
| 化 ↔ 热 | 放热/吸热反应 | `chemical_heat` |

### 5.2 设计原则

1. **先单域后耦合**：先确保每个单域能正确仿真，再加耦合边
2. **时间步统一**：取所有域中最小的 dt 作为全局步长
3. **弱耦合优先**：先用单向耦合（热→力），验证后再加双向

---

## 六、场景模板库

### 6.1 热力学模板

#### 模板 A：简单双节点热传导

```
实体：heater (T=400K) → conductor → sink (T=300K)
边：heater → sink, thermal_conduction
验证：温度趋近平衡 T_eq = (m1·C1·T1 + m2·C2·T2) / (m1·C1 + m2·C2)
用途：验证因果传播方向、能量守恒
```

#### 模板 B：建筑三房间

```
实体：outdoor, wall_north, room_A, inner_wall, room_B
边：6 条 thermal_conduction
验证：温度梯度分布、稳态热流
用途：验证多实体因果图、复杂拓扑
```

#### 模板 C：制冷循环

```
实体：compressor, condenser, expansion_valve, evaporator, cold_room
边：热传导 + 压缩功 + 节流
验证：制冷系数 COP
用途：验证循环因果、能量输入/输出
```

### 6.2 力学模板

#### 模板 D：弹簧-质量系统

```
实体：mass_1, mass_2, wall (固定)
边：wall→m1 (spring), m1→m2 (spring), m1→ground (damping)
验证：固有频率 ω = √(k/m)
用途：验证振动响应、能量守恒
```

### 6.3 复合模板

#### 模板 E：热力耦合

```
实体：heated_rod (热), mass_on_spring (力)
边：thermal_conduction + thermal_expansion
验证：温度升高 → 热膨胀 → 弹簧力变化
用途：验证跨域因果传播
```

---

## 七、因果边的知识来源与置信度标注

> 对应 CDA §6.1.1 KnowledgeDrivenBootstrapper 的置信度层级。

合成数据中的每条因果边必须标注 `source_knowledge` 和 `confidence`，以便 NOTEARS 因果发现算法正确使用先验。

### 7.1 知识来源层级

| `source_knowledge` 值 | 对应 CDA 置信度 | 说明 | 合成数据中的使用场景 |
|-----------------------|----------------|------|-------------------|
| `physics_equation` | 0.95 | 物理方程直接推导（傅里叶定律、牛顿运动方程等） | 基于物理公式生成的因果边 |
| `topology_diagram` | 0.90 | 工程拓扑图（P&ID、电气接线图） | 基于系统拓扑设计的连接关系 |
| `equipment_manual` | 0.80 | 设备手册（型号参数、连接关系） | 空调/散热器等设备参数 |
| `expert_annotation` | 0.60 | 专家标注（因果关系的自然语言描述） | 用户描述的非精确因果关系 |
| `maintenance_log` | 0.40 | 运维日志（异常事件与修复记录） | 历史数据推断的因果关系 |
| `data_inferred` | 0.20 | 从观测数据中自动推断 | 因果发现算法的输出 |

### 7.2 标注规则

**规则 1：物理公式生成的边 → `physics_equation` + confidence 0.95**

```json
{
  "source_id": 0, "target_id": 1,
  "mechanism_type": "thermal_conduction",
  "strength": 0.85,
  "confidence": 0.95,
  "source_knowledge": "physics_equation"
}
```

**规则 2：系统拓扑定义的连接 → `topology_diagram` + confidence 0.90**

```json
{
  "source_id": 1, "target_id": 2,
  "mechanism_type": "thermal_conduction",
  "confidence": 0.90,
  "source_knowledge": "topology_diagram"
}
```

**规则 3：设备控制行为 → `equipment_manual` + confidence 0.80**

```json
{
  "source_id": 2, "target_id": 2,
  "mechanism_type": "thermal_convection",
  "confidence": 0.80,
  "source_knowledge": "equipment_manual"
}
```

**规则 4：不确定性递减**：当同一因果边有多个知识来源时，取最高的置信度。

---

## 八、噪声与不完整性模拟

### 7.1 传感器噪声模型

```python
def add_sensor_noise(trajectory, config):
    """
    config:
      temperature_noise_std: float  # K
      heat_flux_noise_std: float    # W
      missing_probability: float    # 0~1, 每个时间步的缺失概率
      outlier_probability: float    # 0~1, 异常值概率
    """
```

### 7.2 推荐噪声配置

| 场景 | 温度噪声 | 热流噪声 | 缺失率 | 异常率 |
|------|---------|---------|--------|--------|
| 理想验证 | 0.01 K | 0.1 W | 0% | 0% |
| 实验室传感器 | 0.1 K | 1.0 W | 1% | 0.1% |
| 工业传感器 | 0.5 K | 5.0 W | 5% | 1% |
| 恶劣环境 | 1.0 K | 10.0 W | 10% | 5% |

### 7.3 因果边缺失模拟（用于验证因果发现）

故意从 ground truth 图中删除部分边，生成"不完整图"，用于验证 NOTEARS 等因果发现算法能否恢复缺失的边。

```json
{
  "generation_config": {
    "ground_truth_graph": "full.graph.json",
    "edge_removal_rate": 0.3,
    "removed_edges": [
      {"source_id": 0, "target_id": 2},
      {"source_id": 1, "target_id": 3}
    ],
    "purpose": "test_causal_discovery"
  }
}
```
