# 防爆阀设计选型 (Explosion-Proof Valve Selection)

基于 Pack 箱体参数计算所需透气量，并根据压差-透气量特性曲线推荐满足安全约束的防爆阀规格。

## 功能

- **温度变化透气量计算**：基于压差驱动模型，计算升/降温过程中箱体所需的呼吸透气量
- **海拔变化透气量计算**：支持路运（0→3000m）和空运（0→10000m）场景
- **透气系数 K 模型**：`K = V0 / P_ref`，消去温变速率影响，直接给出标化透气量
- **防爆阀选型推荐**：根据压差-流量曲线线性插值，匹配最合适的阀门规格
- **安全约束校验**：阀门排气速率 ≥ 电芯产气速率

## 快速开始

在 WorkBuddy 中安装此 skill 后，通过以下方式触发：

```
@skill:explosion-proof-valve-selection @"path/to/input.xlsx" 选型
```

或者直接描述需求：

```
帮我对 Pack 箱体进行防爆阀选型，V0=59.3L，温度范围-30~55℃，海拔0→10000m
```

## 输入参数

| 参数 | 符号 | 单位 | 说明 |
|------|------|------|------|
| 箱体净容积 | V0 | L | Pack 箱体内部净容积 |
| 温度范围 | T0→T1 | ℃ | 工作温度范围 |
| 温度变化时间 | t | min | 温度从 T0 到 T1 所需时间 |
| 海拔/气压范围 | P0→P1 | kPa 或 m | 运输海拔范围 |
| 电芯产气速率 | G_cell | L/min | 热失控工况下的产气速率 |
| 额定压差 | P_rated | kPa | 防爆阀额定透气量对应的压差（默认 7kPa） |

## 计算原理

### 压差驱动模型（v2）

```
透气系数 K = V0 / P_ref  (L/min per kPa/min)

温度变化: P_ref = P_atm = 101.325 kPa
海拔变化: P_ref = min(P0, P1)，即最低工作气压

标化透气量 @7kPa = K × 7 = V0 / P_ref × 7
```

### 选型约束

```
Φ_valve ≥ max(Φ_breathing, Φ_cell_gas)
安全系数 ≥ 1.5
```

## 文件结构

```
explosion-proof-valve-selection/
├── SKILL.md                    # 技能主文件
├── manifest.yaml               # ClawHub 发布元数据
├── README.md                   # 本文件
├── scripts/
│   └── breathing_calc.py       # 核心计算脚本
└── references/
    ├── formulas.md             # 公式推导与物理模型
    └── valve_data.md           # 阀门特性数据与决策流程
```

## 许可

MIT License
