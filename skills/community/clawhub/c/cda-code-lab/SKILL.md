---
name: cda-code-lab
author: 王教成 Wang Jiaocheng (波动几何)
description: |
  CDA 架构代码工坊——按 Causal Dynamics Architecture 规范生成可执行的 Python 仿真代码。
  覆盖核心组件：CDABlock 管线、PINN 机制函数、哈密顿投影模块、辛积分器、NOTEARS 因果发现、
  贝叶斯在线更新、CER 因果封装递归。
  生成的代码可直接运行，依赖 PyTorch，接受 CDA Data Synthesizer 产出的 JSON 数据作为输入。
  当用户需要实现 CDA 架构组件、生成仿真原型代码、构建因果推理实验时触发。
  触发词：CDA代码、因果动力学实现、CDABlock、哈密顿投影、PINN机制函数、辛积分器、NOTEARS因果发现、CER实现、因果仿真代码。
---

# CDA 架构代码工坊（Code Lab）

将 Causal Dynamics Architecture 的理论设计转化为可执行的 Python 仿真代码。

## 核心定位

CDA 主技能定义了架构蓝图，Data Synthesizer 生成数据，本技能负责**让架构跑起来**。

**数据格式依赖**：本技能生成的代码读取 CDA Data Synthesizer 定义的 JSON 格式（见 `references/data-format-spec.md`）。

## 可生成的组件

按 CDA 五层栈和路线图 Phase 1-2 组织：

### Phase 1 组件（热力学仿真引擎）

| 组件 | CDA 章节 | 输入 | 输出 |
|------|---------|------|------|
| **CDABlock** | §3.2 | EntityState + CausalEdges | 更新后的 EntityState |
| **PINN 机制函数** | §3.3 | 实体状态对 (s_i, s_j) | 状态变化量 Δs |
| **哈密顿投影** | §4.1 | 状态 (q, p) | 约束后状态 |
| **辛积分器** | §4.2 | 状态 + 力函数 | 下一时刻状态 |
| **贝叶斯状态更新** | §6.2 L1 | 旧信念 + 观测 | 新信念 |
| **JSON 数据加载器** | — | *.graph.json / *.trajectory.json | Python 对象 |

### Phase 2 组件（多域因果耦合）

| 组件 | CDA 章节 | 说明 |
|------|---------|------|
| **机制类型注册表** | §3.3.1 | 力学/热力学/流体/化学反应类型的 W 矩阵约束 |
| **因果计算路由** | §3.4 | 稀疏边选择（路由分数 → Top-K → 预算） |
| **NOTEARS 因果发现** | §6.1.2 | 从时序数据中学习因果结构 |
| **在线 Laplace 学习** | §6.2 L2 | 机制函数参数的在线贝叶斯更新 |
| **粗粒化 + 重正化** | §7 | 信息瓶颈驱动的实体聚合 |

### 高级组件（Phase 3-4）

> 以下组件对应 CDA 主参考文档的深层章节（§5 do-演算、§7 多尺度、§8 CER），
> 属于路线图 Phase 3（反事实推理与决策，2-4 年）和 Phase 4（通用因果世界模型，4-8 年）。
> 当前 SKILL.md 和 references 中的 Phase 1-2 组件已覆盖核心计算原语。
> 当用户请求实现以下组件时，应先加载 CDA 主技能的参考文档对应章节获取完整规格。

| 组件 | CDA 章节 | Phase | 说明 |
|------|---------|-------|------|
| **do-演算图手术** | §五 | 3 | 干预推理：切断因果边 + 传播 |
| **反事实推理** | §五 | 3 | 溯因→干预→预测三步 |
| **CER 因果封装递归** | §八 | 4 | 异构嵌套因果子系统（CDA 最原创贡献） |
| **多尺度聚合** | §七 | 3 | 自适应分辨率切换（粗粒化 + 重正化） |
| **量纲一致性模块** | §3.3.2 / §4.4 | 2 | 禁止跨量纲的参数耦合（物理量纲通道） |
| **感知校准层** | §2.1-2.2 | 4 | 统一感知接口 + 贝叶斯校准 |

## 参考文件

| 文件 | 内容 |
|------|------|
| `references/implementation-guide.md` | **核心指南**：代码架构设计、依赖管理、运行约定 |
| `references/component-specs.md` | 每个组件的接口签名、输入输出规格、实现要点 |
| `references/pinn-templates.md` | PINN 机制函数的 PyTorch 模板（热力学/力学/流体） |
| `references/data-format-spec.md` | 数据格式协议（从 Data Synthesizer 共享，本文件为副本） |

## 代码生成原则

1. **PyTorch 优先**：所有可微分组件使用 PyTorch 实现，确保自动微分可用
2. **JSON 兼容**：生成的代码必须能直接读取 Data Synthesizer 的 JSON 输出
3. **可验证**：每个组件附带 self-test 函数，使用合成数据验证正确性
4. **渐进复杂度**：先生成最小可运行版本（单组件），再组合完整管线
5. **物理硬约束**：哈密顿投影、辛积分器等不可用 soft constraint 替代

## 典型生成流程

```
用户请求："实现热力学仿真引擎"
  ↓
1. 读取 implementation-guide.md → 确定项目结构和依赖
  ↓
2. 读取 component-specs.md → 确定需要哪些组件
  ↓
3. 读取 pinn-templates.md → 获取机制函数模板
  ↓
4. 生成代码文件：
   ├── data_loader.py    （JSON → EntityState/CausalEdge）
   ├── entities.py       （EntityState, CausalEdge, WorldState 类）
   ├── mechanisms.py     （PINN 机制函数）
   ├── hamiltonian.py    （哈密顿投影）
   ├── integrator.py     （辛积分器）
   ├── cdablock.py       （完整管线）
   └── run_simulation.py （主入口 + 示例）
  ↓
5. 生成 self_test.py → 验证每个组件
```

## 与 CDA 主技能的关系

```
CDA（主技能）
  ├── 理论参考：架构设计、公式、路线图
  ├── CDA Data Synthesizer
  │     └── 生成 JSON 格式的因果数据集
  └── CDA Code Lab（本技能）
        └── 生成代码：读取 JSON → 运行仿真 → 输出结果
```

## 使用指南

1. 用户指定要实现的组件或场景
2. 读取 `references/implementation-guide.md` 获取代码架构
3. 读取 `references/component-specs.md` 获取组件接口规格
4. 根据域类型读取 `references/pinn-templates.md` 获取机制函数模板
5. 生成完整的 Python 代码文件，附带注释和 self-test
