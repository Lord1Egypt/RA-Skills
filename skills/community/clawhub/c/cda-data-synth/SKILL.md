---
name: cda-data-synth
author: 王教成 Wang Jiaocheng (波动几何)
description: |
  CDA 因果数据合成器——根据领域描述自动生成 CDA 架构可消费的因果数据集。
  生成 Entity-State Graph（JSON 格式）、CausalEdge 列表、带时间戳的观测轨迹、哈密顿量约束参数。
  覆盖热力学、力学、流体、多域耦合等物理域，支持生成训练数据、验证数据、基准测试数据。
  当用户需要为 CDA 架构生成合成数据、构造因果仿真场景、设计测试基准数据集时触发。
  触发词：因果数据合成、Entity-State Graph、生成仿真数据、CDA训练数据、合成因果数据、因果图数据、物理仿真数据集、因果轨迹数据。
---

# CDA 因果数据合成器（Data Synthesizer）

为 Causal Dynamics Architecture 架构生成标准格式的合成因果数据集。

## 核心定位

CDA 架构的输入不是 Token 序列，而是 **Entity-State Graph**（实体-状态因果图）。本技能解决从"领域描述"到"架构可消费数据"的桥梁问题。

**数据格式所有权**：本技能定义并维护 CDA 的数据序列化协议。Code Lab 技能依赖此协议生成代码。

## 工作流程

```
用户描述场景
  ↓
1. 解析领域类型（热力学/力学/流体/多域耦合）
  ↓
2. 设计实体拓扑（entities + edges 骨架）
  ↓
3. 参数化机制函数（mechanism parameters）
  ↓
4. 运行前向仿真生成轨迹（trajectory snapshots）
  ↓
5. 序列化为 JSON 格式输出
```

## 输出格式规范

所有输出必须符合 `references/data-format-spec.md` 中定义的 JSON Schema。

核心输出文件类型：
- `*.graph.json` — 静态因果图（实体 + 边 + 属性）
- `*.trajectory.json` — 时序轨迹（多时刻快照序列）
- `*.hamiltonian.json` — 哈密顿量参数（势能函数 + 守恒量）
- `*.meta.json` — 数据集元信息（域类型、规模、物理约束摘要）

## 参考文件

| 文件 | 内容 |
|------|------|
| `references/data-format-spec.md` | **核心协议**：Entity-State Graph 的完整 JSON Schema 定义 |
| `references/synthesis-protocols.md` | 各物理域的数据合成协议（热力学/力学/流体/耦合） |
| `references/thermal-building-example.json` | 热力学示例：建筑温度仿真数据集 |

## 数据合成原则

1. **物理一致性**：合成数据必须满足能量守恒、质量守恒等物理约束
2. **因果真实性**：因果边的方向和机制函数必须反映真实物理规律
3. **可验证性**：每条因果边都附带 ground truth，便于验证因果发现算法
4. **可扩展性**：从简单场景（3-5 实体）到复杂场景（100+ 实体）渐进生成

## 域类型与对应的物理约束

| 域 | 广义坐标 q | 共轭动量 p | 典型机制函数 | 守恒量 |
|----|-----------|-----------|-------------|--------|
| 热力学 | 温度 T | 热流 J_q | 傅里叶定律、牛顿冷却 | 能量 |
| 力学 | 位移 x | 动量 p | 胡克定律、阻尼力 | 能量、动量 |
| 流体 | 压力场 P | 质量流 J_m | Navier-Stokes 简化 | 质量、动量 |
| 电路 | 电荷 Q | 电流 I | 欧姆定律、基尔霍夫定律 | 电荷、能量 |

## 与 CDA 主技能的关系

```
CDA（主技能）
  ├── 理论参考：架构设计、公式、路线图
  ├── CDA Data Synthesizer（本技能）
  │     └── 数据生成：Entity-State Graph → JSON
  └── CDA Code Lab
        └── 代码生成：读取数据 → 仿真/训练代码
```

## 使用指南

1. 用户描述目标场景（如"一个有三台压缩机和两个冷库的制冷系统"）
2. 读取 `references/data-format-spec.md` 获取格式规范
3. 读取 `references/synthesis-protocols.md` 获取对应域的合成协议
4. 参考示例文件了解完整数据集结构
5. 生成符合规范的 JSON 数据文件，输出到用户指定目录
