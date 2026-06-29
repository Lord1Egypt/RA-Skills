# AI CGO — AI Chief Growth Officer

> **AI驱动的企业增长操作系统** — 增长决策系统 + AI工作流编排器 + 自动优化引擎

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

## 为什么需要 AI CGO？

Prompt 是静态配置。模型升级、市场变化、用户需求变化都会让 Prompt 老化。

**AI CGO 是一个结构化积累知识的 Skill** — 每次对话可沉淀经验到知识库，供后续对话参考。

## 架构

```
User Input → Router → Diagnoser (增长问题诊断)
                    → Designer (机会探索 / 工作流设计)
                    → Optimizer (审计与优化)
                    │
                    ▼
            Self-Validation (6项质量门控)
                    │
            GO / WARN / BLOCK
                    │
                    ▼
            Execution Metrics + Trace
                    │
                    ▼
            Optimization Protocol → kb.md 沉淀
```

## 三大模式

### Diagnoser — 增长问题诊断

六段式输出：**诊断 → 机会 → 工作流 → 自动化 → KPI → 实验循环**

聚焦一个核心瓶颈，量化影响，给出可执行方案。

### Designer — 机会探索 / 工作流设计

- **机会探索**：机会地图 + Use Case Cards + 优先级矩阵
- **工作流设计**：Agent 架构 + 组件规格 + 实施路线图 + 成本模型

### Optimizer — 审计与优化

审计现有漏斗/系统 → 优先级修复计划 → AI 改造点 → 预期改善度量

## 知识沉淀机制

| 机制 | 作用 |
|------|------|
| **Self-Validation Protocol** | 6 项质量门控，输出交付前自动验证，GO/WARN/BLOCK 三级决策 |
| **Execution Metrics** | 每次输出强制附带 6 项指标（路由、置信度、指标引用、假设、后续行动、轮次） |
| **Runtime Trace** | 全决策链路结构化追踪（Router → Self-Check → Validation → Output → Optimization） |
| **Optimization Protocol** | 满意→知识沉淀到 kb.md / 不满意→诊断归因到失败模式 |
| **Feedback Classification** | 将用户反馈归类为 6 类信号，用于辅助改进 |
| **learnings/ 知识库** | 成功模式、失败模式、行业基准、策略模式的共享记录 |

## 目录结构

```
ai-cgo/
├── SKILL.md                          # 主技能文件（Router + 3模式 + 知识沉淀）
├── README.md                         # 本文件
├── learnings/                        # 知识库（手动维护，随使用积累）
│   ├── kb.md                         # 成功/失败模式、行业基准、策略模式
│   └── router-signals.md             # 动态路由信号表（可运行时扩展）
└── references/                       # 参考文档（按需加载）
    ├── capability-model.md           # 6层CGO能力模型
    ├── harness-engineering.md          # Harness工程框架（R.E.S.T + PPAF）
    └── workflow-design.md            # AARRR各阶段工作流模式
```

## 参考文档

| 文档 | 用途 |
|------|------|
| [capability-model.md](references/capability-model.md) | 6层CGO能力模型：增长策略→AI系统能力→执行→数据飞轮→组织→进阶 |
| [harness-engineering.md](references/harness-engineering.md) | Harness工程框架：R.E.S.T.模型 + PPAF Agent循环 + 安全约束 |
| [workflow-design.md](references/workflow-design.md) | AARRR各阶段工作流模式 + Agent编排模式 |
| [learnings/kb.md](learnings/kb.md) | 知识库：成功/失败模式、行业基准、策略模式（随使用积累） |
| [learnings/router-signals.md](learnings/router-signals.md) | 动态路由信号表（可运行时扩展） |

## 触发场景

- 分析业务增长瓶颈并制定AI增长策略
- 设计AI驱动的工作流和自动化增长系统
- 用AI重构营销、销售、转化流程
- 建立增长数据飞轮和KPI体系
- 规划Multi-Agent增长系统架构
- 企业AI转型增长落地咨询

## 快速开始

### 作为 Skill 使用

将 `ai-cgo` 目录导入以下平台即可使用：

- **Trae** — 放入 `.trae/skills/` 目录
- **OpenClaw** — 放入 skills 目录
- **Hermes Agent** — 放入 skills 目录

### 触发方式

直接输入以下任一关键词即可激活：

- 增长策略、AI增长、怎么用AI赚钱、增长系统、增长工作流
- AI营销系统、转化优化、增长飞轮、AI CGO、增长漏斗、增长瓶颈
- 怎么提升转化、AI业务落地

### 输入要求

**必需信息：** 业务背景（商业模式、行业、阶段）、增长挑战（具体指标或问题）

**可选信息：** 预算、CAC、LTV、竞品列表

## 排除场景（不触发）

以下场景会路由到其他 Skill：

| 场景 | 路由到 |
|------|--------|
| 纯品牌定位/品牌VI设计 | `4aos` 或 `brand-marketing-plan` |
| 纯社交媒体内容/运营/KOL | `mktclaw` |
| 纯广告创意/媒体投放/Campaign策划 | `4aos` |
| 无需增长策略的纯技术开发咨询 | 不触发 |

## License

Apache-2.0
