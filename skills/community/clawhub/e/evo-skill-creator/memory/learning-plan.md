# 学习计划

> evo-skill-creator 的学习计划。仅包含需要"学习/研究"的项目。
> 待办任务（需要"做"的事）见 `backlog.md`。
> 上次审视：2026-04-04（plan 命令）

## 优先级说明

- **P0**：直接影响创建子智能体质量的核心知识，必须优先深入
- **P1**：重要但非紧急，影响进化模型的架构决策
- **P2**：有价值但可延后，扩展视野或应对未来挑战
- **P3**：远期探索，理论前沿或小众方向

## 待学习

### 49. EvoSkill — 失败驱动的自动技能发现与精炼框架（P0）
- **来源**：2026-04-03 plan 搜索发现（arXiv 2026-03-03）
- **知识沉淀**：`memory/knowledge/agent-design/evoskill-failure-driven-skill-discovery-2026.md`
- **学习次数**：1（2026-04-03 深度学习）
- **状态**：已完成首轮
- **核心收获**：
  - 三角色架构（Executor→Proposer→Skill-Builder）映射到我们的 go→review→go 命令，关键差距是 review 缺少"失败诊断"
  - Pareto 前沿 = 动态版退化防护，比我们的静态检查清单更强——需要为子智能体建立"基准场景集"
  - Skill Folder 结构（SKILL.md + 触发元数据 + Helper Scripts）与我们完全兼容
  - search-persistence-protocol 的零样本迁移证明：最有价值的技能是"抽象方法论"而非"具体代码"
  - knowledge/ 应区分被动知识（theory/）和主动技能（skills/），后者需要触发条件
- **后续行动**：
  - review 命令增加"失败诊断"维度（分析 execution.log 中的低效模式）→ 纳入 backlog
  - 为子智能体定义基准场景集（3-5 个典型场景，升级后验证）→ 纳入 backlog
  - knowledge/ 目录分类升级（被动知识 vs 主动技能）→ 中期规划

### 50. Hindsight — 四网络结构化记忆架构（P1）
- **来源**：2026-04-03 plan 搜索发现（arXiv:2512.12818，Vectorize + Virginia Tech）
- **知识沉淀**：待创建 `memory/knowledge/agent-design/hindsight-structured-memory-architecture-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：Hindsight 将记忆分为四个语义网络（World/Experience/Observation/Opinion），核心创新是**事实与信念的显式分离** + 可配置性格参数（skeptical/empathetic）。与我们的 memory 架构设计高度相关：
  1. 我们的 knowledge/ 目录混合了事实（API 文档）和观点（设计决策），缺乏显式分类
  2. opinion 网络带 confidence score 的演化更新——类似我们的 evolution-log 但更结构化
  3. Retain-Recall-Reflect 三操作与我们的 learn-go-review 有映射关系
- **关键问题**：
  - 四网络模型如何映射到我们的 memory/ 目录结构？是否需要增加 opinion/ 或 experience/ 子目录？
  - Confidence score 机制对 knowledge/ 下的文件管理有什么启发？
  - "可配置性格参数"对不同角色（严谨工程师 vs 感性作家）的记忆策略有什么启发？
- **后续**：可能需要升级 evo-agent-model.md 的 Memory 目录结构标准

### 51. Letta — Self-Editing Memory 与 Agent 自主上下文管理（P1）
- **来源**：2026-04-03 plan 搜索发现（原 MemGPT 概念的产品化实现）
- **知识沉淀**：待创建 `memory/knowledge/agent-design/letta-self-editing-memory-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：Letta 的核心思想是让 Agent 自主决定上下文窗口内容（core memory vs archive），借鉴 OS 的内存管理（RAM vs Disk）。这与我们的 scene-index.md 机制高度相关——我们用手动索引决定加载什么，Letta 让 Agent 自己决定。
- **关键问题**：
  - Self-editing memory 的"主动遗忘/归档"决策机制是什么？
  - 与我们的 scene-index.md（手动索引）相比，自动化的上下文管理是否更优？
  - core memory（RAM）vs archive（Disk）的分界线如何定义？
  - 对 backlog #3（memory 容量管理策略）有什么直接启发？
- **后续**：直接应用到 backlog #3 和 scene-index.md 机制升级

### 41. AVO + 受限自我进化退化防护设计（P1）— **已合并两个重复 #41**
- **来源**：2026-03-30 learn + 2026-03-31 plan + 2026-04-01 learn
- **知识沉淀**：`memory/knowledge/agent-design/agentic-variation-operators-avo-2026.md` + `constrained-self-evolution-framework-2026.md`
- **学习次数**：1（2026-04-01 深度学习，合并 AVO 工程实践与退化防护理论）
- **状态**：已完成首轮
- **核心收获**：
  - AVO 的自导向循环（plan→implement→test→debug）映射到我们的 go→review，关键差距是"进化谱系查询"
  - evolution-log 应从审计日志升级为进化决策输入
  - 知识库的战略价值得到 AVO 实践验证（Agent 查询领域知识指导变异）
  - 即时反馈 vs 事后评审——go 命令应嵌入即时质量检查
- **未解决问题**（可升级为独立学习项）：
  - 退化防护章节的具体阈值和触发机制设计
  - review 命令的双重角色（进化推进 + 退化检测）如何平衡

### 42. 可靠执行器架构与 Agent-as-System 范式（P1）
- **来源**：2026-03-31 plan 搜索发现
- **知识沉淀**：`memory/knowledge/agent-design/reliable-executor-agent-as-system-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：2026 行业共识从 "Agent as Prompt" 转向 "Agent as System"。生产级 Agent 要求：graph-based 编排 + 检查点 + 隔离环境 + 行为可观测性。我们的 scheduler + execution.log 是轻量实现，但与生产级标准差距大。
- **关键问题**：
  - Graph-based 编排（LangGraph 状态机）如何映射到我们的命令体系？
  - 检查点（Checkpointing）对长时间运行的 learn/scan 有什么价值？
  - 行为可观测性（Behavioral Observability）vs 我们的命令级日志——差距有多大？
  - 隔离执行环境对 scheduler 调度有什么启发？
- **后续**：与 #21（Agent Observability）和 #39（Durable Execution）结合

### 43. SKILL.md YAML Frontmatter 与发现机制标准化（P1）
- **来源**：2026-03-31 plan + 2026-04-01 learn（agentskills.io 标准研究）
- **知识沉淀**：`memory/knowledge/frameworks/skill-yaml-frontmatter-discovery-2026.md`
- **学习次数**：1（2026-04-01 深度学习）
- **状态**：已完成首轮
- **核心收获**：
  - 标准字段：name（必选，匹配目录名）、description（必选，含触发短语）、license、compatibility、metadata（含 version/author/tags）
  - 无独立 triggers 字段，路由完全依赖 description 的自然语言
  - 渐进式披露三级：启动加载 name+desc → 触发加载 body → 执行加载 scripts/references
  - 我们的子智能体大部分缺少 frontmatter，需要补充
- **后续行动**：写入 evo-agent-model.md 模板 + 纳入创建检查清单 + 为现有子智能体补充

### 44. Claude Tasks + Agent Teams 持久化多 Agent 协作架构（P1）
- **来源**：2026-03-31 scan 发现
- **知识沉淀**：`memory/knowledge/frameworks/claude-tasks-agent-teams-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：Claude Code 原生支持持久化任务状态（文件系统级）和并行多 Agent 协作。直接影响：(1) steward 的并行唤醒设计 (2) scheduler 的状态持久化 (3) 跨会话任务协调。这是 Anthropic 官方的生产级 Agent 基础设施，比我们的轻量 cron 方案更成熟。
- **关键问题**：
  - Claude Tasks 的文件系统状态格式是什么？能否与我们的 execution.log 统一？
  - Agent Teams 的并行执行 + 相互校验模式如何映射到 steward 的代理唤醒？
  - CLAUDE_CODE_TASK_LIST_ID 跨会话协调对多智能体生态有什么价值？
  - 我们是否需要让 scheduler 利用 Claude Tasks 而非自行管理状态？
- **后续**：可能需要升级 steward 和 evo-skills-maintainer 的架构设计

### 45. Agent Trajectory Evaluation 与 DAG Metrics（P1）
- **来源**：2026-03-31 scan 发现
- **知识沉淀**：`memory/knowledge/agent-design/trajectory-evaluation-dag-metrics-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：生产级 Agent 评估已从"结果正确"转向"推理路径最优+多次运行一致"。DeepEval 的 DAG Metrics 将评估标准映射到执行图。我们的 review 命令需要一个结构化评审框架，而不是靠 LLM 主观判断。
- **关键问题**：
  - 如何将 Trajectory Evaluation 的思路应用到 review 命令的评审维度？
  - execution.log 需要记录什么粒度的信息才能支持轨迹评估？
  - DeepEval DAG Metrics 如何映射到我们的命令执行图？
  - Cronbach's alpha（多次运行一致性）对我们意味着什么——是否需要对关键命令做重复执行验证？
- **后续**：直接应用到 backlog #10（review 命令评审维度定义）

### 46/60. Skill 开源全流程与市场化分发（P0）→ **已完成首轮**
- **来源**：2026-03-31 scan 发现 + 2026-04-05 learn（扩展为开源全流程）
- **知识沉淀**：`memory/knowledge/frameworks/skill-opensource-requirements-2026.md`
- **学习次数**：1（2026-04-05 深度学习）
- **状态**：已完成首轮
- **核心收获**：
  - 通用开源要求：LICENSE（建议 Apache 2.0）、CONTRIBUTING.md、CODE_OF_CONDUCT.md、SECURITY.md
  - Skill 特有要求：YAML frontmatter（#43）、skills.sh 兼容结构、README 英文化
  - **有状态智能体的特殊挑战**（核心发现）：开源的是框架而非实例，memory/private/ + output/ 必须排除
  - knowledge/ 策略需决策（精选开源 vs 完全开源 vs 留空让用户自己 learn）
  - 路径脱敏是最大工程量：SKILL.md 中绝对路径→相对路径/模板变量
  - 提出五阶段开源检查清单：代码脱敏→标准文件→Skill 标准化→文档完善→仓库准备
- **后续行动**：直接作为 review 命令评审开源准备度的依据

### 33. OpenSpace Self-Evolving Skill Engine（P2）
- **来源**：2026-03-29 plan 搜索发现
- **知识沉淀**：`memory/knowledge/frameworks/openspace-self-evolving-skill-engine-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：OpenSpace 推出的自我进化 Skill 引擎，这是商业产品级别的自我进化实现，值得研究其设计思路和商业化路径。
- **关键问题**：
  - OpenSpace 的自我进化机制是什么？
  - 与学术界的 DGM、EvoAgentX 等框架有什么区别？
  - 商业产品如何平衡进化能力和稳定性？
- **后续**：可能为我们的商业化提供参考

### 34. SkillNet - Open Infrastructure to Eliminate AI Agent Redundancy（P2）
- **来源**：2026-03-29 plan 搜索发现
- **知识沉淀**：`memory/knowledge/agent-design/skillnet-open-infrastructure-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：SkillNet 是一个开放基础设施，旨在消除 AI Agent 冗余，这与我们的 agents-registry 和能力发现机制相关。
- **关键问题**：
  - SkillNet 如何识别和消除 Agent 冗余？
  - 开放基础设施的架构是什么？
  - 如何与我们的 agents-registry 集成？
- **后续**：可能需要为 agents-registry 增加"能力去重"功能

### 35. Octopoda - Unified Infrastructure for AI Agent Memory and Observability（P2）
- **来源**：2026-03-29 plan 搜索发现
- **知识沉淀**：`memory/knowledge/agent-design/octopoda-unified-infrastructure-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：统一的 Agent Memory 和可观测性基础设施，这与我们的 Memory 架构（#22）和 Observability 需求（#21）都相关。
- **关键问题**：
  - Octopoda 如何统一 Memory 和 Observability？
  - 与我们的文件系统级 memory + execution.log 如何对比？
  - 是否需要引入统一基础设施？
- **后续**：可能需要升级我们的可观测性架构

### 37. HiMAC — 层级化宏观-微观长期任务架构（P2）
- **来源**：2026-03-30 scan 发现（arXiv:2603.00977）
- **知识沉淀**：`memory/knowledge/agent-design/himac-hierarchical-macro-micro-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：将 Agent 决策分为宏观策略（规划蓝图）+ 微观执行（原子动作），通过迭代共同进化训练解决长期任务。与我们的 go 命令中"推断目标→定义工作流→执行"的模式类似，但更系统化。
- **关键问题**：
  - Critic-Free 层级策略优化是否可以映射到我们的 review 评估机制？
  - Macro-Exploration + Micro-Adaptation 交替训练如何启发我们的 learn/scan + go 交替模式？
  - 在 ALFWorld/WebShop 上的实验结果对我们设计子智能体有什么参考价值？

### 39. Durable Execution for AI Agents — 持久执行架构（P2）
- **来源**：2026-03-30 scan 发现
- **知识沉淀**：`memory/knowledge/agent-design/durable-execution-agents-2026.md`
- **学习次数**：0
- **状态**：待学习（浅层理解已有）
- **为什么重要**：我们的 scheduler 是轻量级 cron 调度，但真正的生产级 Agent 需要持久执行——状态持久化 + 事件历史回放 + 故障恢复。Temporal 框架的思路与我们的 execution.log 有相似之处（append-only 日志），但成熟度差距大。
- **关键问题**：
  - Temporal 的事件历史回放如何映射到我们的 execution.log？
  - 是否需要为 scheduler 增加检查点和恢复机制？
  - 幂等性设计对 cron 任务意味着什么——重复执行 learn 是否安全？

### 45. 知识沉淀质量约束体系研究（P1）
- **来源**：2026-03-31 tech-solver 实践反馈 + 2026-04-01 learn（综合分析）
- **知识沉淀**：`memory/knowledge/agent-design/knowledge-quality-constraints-2026.md`
- **学习次数**：1（2026-04-01 深度学习）
- **状态**：已完成首轮
- **核心收获**：
  - 7 大质量维度：抽象优先（已实施）、过时检测、冗余检测、冲突解决、粒度控制、引用溯源、实践验证
  - 前 4 个防止退化，后 3 个提升价值
  - 知识库面临与代码库相同的退化风险（SlopCodeBench 类比）
  - learn 命令应增加查重步骤；review 命令应增加知识库健康扫描
- **后续行动**：将立即可做的 3 项（查重/元数据/冲突标记）写入 evo-agent-model.md

### 47. 生产级多 Agent 编排模式与框架实践（P1）
- **来源**：2026-04-01 scan 发现
- **知识沉淀**：`memory/knowledge/agent-design/production-multi-agent-orchestration-2026.md`
- **学习次数**：1（2026-04-02 深度学习）
- **状态**：已完成首轮
- **核心收获**：
  - 四大编排模式（Sequential/Parallel/Hierarchical/Collaborative）各有适用场景，不是越复杂越好
  - "Multi-Agent Trap" 是 2026 重要反思——Cognition 公开表示不用多 Agent，关键是任务粒度匹配
  - LangGraph 是生产级首选，但检查点 ≠ 持久执行（Diagrid 论点），Dapr Agents 1.0 代表真正的持久执行
  - 混合架构成为主流：CrewAI（发现/推理）→ LangGraph（执行/控制）
  - 我们的 scheduler 定位（轻量级 cron）是正确的，不需要变成 LangGraph
  - steward 可借鉴并行模式、review 可借鉴协作模式
- **未解决问题**：
  - execution.log 结构化升级的具体字段设计
  - steward 并行唤醒的实现细节

### 48. AgentOps 与生产级可观测性实践（P1）
- **来源**：2026-04-01 scan 发现
- **知识沉淀**：`memory/knowledge/agent-design/agentops-production-observability-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：生产级 Agent 需要完整的可观测性栈：Tracing（轨迹追踪）+ Metrics（指标监控）+ Logging（日志）+ Evaluation（评估）。我们的 execution.log 是轻量级日志，但与生产标准（AgentOps/LangSmith/Arize Phoenix）差距大。
- **关键问题**：
  - AgentOps 的 Tracing 标准是什么？如何追踪跨命令的执行轨迹？
  - 我们的 execution.log 应该记录什么粒度的信息才能支持生产级可观测性？
  - Metrics 维度有哪些？（延迟/成本/成功率/Token 消耗/工具调用次数）
  - Evaluation 如何集成到 CI/CD？与 review 命令的关系是什么？
- **后续**：直接应用到 execution.log 格式升级和 review 命令评估维度定义

## 已完成（首轮）

> 以下项目已完成至少一轮学习，知识已沉淀到对应文件。需要深入时可升级回「待学习」。

| # | 主题 | 优先级 | 学习次数 | 知识文件 |
|---|------|--------|----------|----------|
| 49 | EvoSkill — 失败驱动的自动技能发现与精炼 | P0 | 1 | `agent-design/evoskill-failure-driven-skill-discovery-2026.md` |
| 47 | 生产级多 Agent 编排模式与框架实践 | P1 | 1 | `agent-design/production-multi-agent-orchestration-2026.md` |
| 41 | AVO + 受限自我进化退化防护 | P1 | 1 | `agent-design/agentic-variation-operators-avo-2026.md` |
| 43 | SKILL.md YAML Frontmatter 标准 | P1 | 1 | `frameworks/skill-yaml-frontmatter-discovery-2026.md` |
| 45 | 知识沉淀质量约束体系 | P1 | 1 | `agent-design/knowledge-quality-constraints-2026.md` |
| 40 | Constrained Self-Evolution Framework | P0 | 1 | `agent-design/constrained-self-evolution-framework-2026.md` |
| 29 | Anthropic Modular Skill Architecture | P0 | 1 | `frameworks/anthropic-modular-skill-architecture-2026.md` |
| 30 | AgentSkillOS — Ecosystem Scale | P0 | 1 | `agent-design/agent-skills-ecosystem-scale-2026.md` |
| 31 | MemMA — Memory Cycle Coordination | P1 | 1 | `agent-design/memma-memory-cycle-coordination-2026.md` |
| 32 | Hermes Agent Hybrid Memory | P1 | 1 | `frameworks/hermes-agent-hybrid-memory-2026.md` |
| 36 | HyperAgents — DGM-H Cross-Domain | P1 | 1 | `agent-design/hyperagents-dgm-h-cross-domain-2026.md` |
| 38 | SlopCodeBench — Structural Erosion | P1 | 1 | `agent-design/slopcodebench-structural-erosion-2026.md` |
| 26 | EvolveR — Experience-Driven Lifecycle | P1 | 1 | `agent-design/evolver-experience-driven-lifecycle-2026.md` |
| 27 | Self-Referential Agent Framework | P1 | 1 | `agent-design/self-referential-agent-framework-2026.md` |
| 28 | Meta Context Engineering (MCE) | P1 | 1 | `agent-design/meta-context-engineering-2026.md` |
| 22 | Agent Memory Cost Optimization | P1 | 1 | `agent-design/agent-memory-cost-optimization-2026.md` |
| 23 | Karpathy Loop — Autonomous Experimentation | P1 | 1 | `agent-design/karpathy-loop-autonomous-experimentation-2026.md` |
| 24 | NVIDIA Open Agent Platform | P1 | 1 | `agent-design/nvidia-open-agent-platform-2026.md` |
| 25 | DGM-Hyperagents — Self-Rewriting | P1 | 1 | `agent-design/dgm-hyperagents-self-rewriting-2026.md` |
| 19 | Files vs Database Memory Debate | P1 | 1 | `agent-design/files-vs-database-memory-debate-2026.md` |
| 20 | Markdown Systems Scaling Challenges | P2 | 1 | `agent-design/markdown-systems-scaling-challenges-2026.md` |
| 21 | Agent Observability Taxonomy | P1 | 1 | `agent-design/agent-observability-taxonomy-2026.md` |
| 17 | Meta-Agent & Recursive Improvement | P1 | 1 | `agent-design/meta-agent-recursive-improvement.md` |
| 18 | File-Based Memory Architecture | P1 | 1 | `agent-design/file-based-memory-architecture.md` |
| 15 | Context Window Illusion & Memory OS | P1 | 1 | `agent-design/context-window-illusion.md` |
| 16 | Self-Consolidation Mechanism | P1 | 1 | `agent-design/self-consolidation-mechanism.md` |
| 11 | Context Engineering | P1 | 1 | `agent-design/context-engineering.md` |
| 12 | Multi-Agent Context Sharing | P2 | 1 | `agent-design/multi-agent-context-sharing.md` |
| 13 | Knowledge Lifecycle Management | P2 | 1 | `agent-design/knowledge-lifecycle-management.md` |
| 14 | A2A Agent Card & Capability Discovery | P3 | 1 | `agent-design/a2a-agent-card-capability-discovery.md` |
| 7 | Auto Tick — Desktop/Cloud Scheduling | P1 | 1 | `agent-design/auto-tick-mechanism.md` |
| 2 | Skill Evolution Limitations | P1 | 1 | `agent-design/skill-evolution-limitations.md` |
| 5 | Darwin Gödel Machine (DGM) | P3 | 1 | `frameworks/darwin-godel-machine.md` |
| 6 | Framed Autonomy & Hierarchical Design | P3 | 1 | `agent-design/framed-autonomy-hierarchical-design.md` |

## 已完成（深度研究）

| # | 主题 | 优先级 | 学习次数 | 知识文件 |
|---|------|--------|----------|----------|
| 1 | Memento-Skills Framework | P1 | 2 | `frameworks/memento-skills.md` |
| 8 | Skill Routing & SkillOrchestra | P1 | 2 | `agent-design/skill-routing/` |
| 9 | Auto Skill Assessment Framework | P2 | 2 | `agent-design/auto-skill-assessment-framework.md` |
| 10 | On-Demand Skill Loading | P1 | 1 | `agent-design/2026-agent-skills-developments.md` |
| 3 | SAGE Memory Management | P2 | 1 | `frameworks/sage-memory-management.md` |
| 4 | EvoAgentX Framework | P2 | 1 | `frameworks/evoagentx.md` |

### 52. Prompt-Shape Surgery 与轮次边界退化防护（P1）
- **来源**：2026-04-03 scan 发现
- **知识沉淀**：待创建 `memory/knowledge/agent-design/prompt-shape-surgery-turn-boundary-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：模型在提示形状模拟"轮次边界"时过早停止或产生幻觉，是代码质量退化的新根因。纯 prompt 优化无法解决，需要系统级的提示形状工程。
- **关键问题**：
  - 轮次边界误判在长 SKILL.md 指令中的发生频率和条件？
  - 非空标记（如 `[Tool Loaded]`）的最佳实践是什么？
  - 与结构化输出强制（JSON/tool-use mode）的组合效果？
  - 子智能体的 SKILL.md 是否需要加入轮次边界安全标记？
- **后续**：可能需要更新 evo-agent-model.md 的 SKILL.md 模板

### 53. Clean-Room Agent Pattern 与隔离验证模式（P2）
- **来源**：2026-04-03 scan 发现
- **知识沉淀**：待创建 `memory/knowledge/agent-design/clean-room-agent-pattern-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：高风险重构场景下，Specifier-Implementer 分离模式防止 Agent 在修改已理解偏差的代码时产生"漂移"。与 Generator-Evaluator Loops 互补，但更聚焦于防止认知漂移。
- **关键问题**：
  - Clean-Room 模式的开销（双 Agent 调用）在什么规模的任务下值得？
  - 如何与我们的 review 命令集成——review 是否应该扮演 Specifier 角色？
  - 与 brainstorming skill 的关系——brainstorming 是否已经是隐式的 Specifier？
- **后续**：可能影响 go 命令的创建流程设计

### 54. Agent 安全架构：IAM 集成与 Memory Poisoning 防护（P2）
- **来源**：2026-04-03 scan 发现
- **知识沉淀**：待创建 `memory/knowledge/agent-design/agent-security-iam-memory-poisoning-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：Agent 被分配数字身份和权限范围，记忆成为攻击面。我们的 `.claude/settings.local.json` 是轻量级权限控制，但 memory/private/ 的安全性和子智能体间数据隔离需要系统性思考。
- **关键问题**：
  - 我们的权限模型（settings.local.json）与企业级 IAM 的差距有多大？
  - memory/private/ 的完整性如何保证？是否需要签名或哈希校验？
  - 子智能体间是否存在通过 shared memory 进行"投毒"的风险？
  - 零信任架构下，steward 代理唤醒子智能体的安全边界如何定义？
- **后续**：可能需要在 evo-agent-model.md 中增加安全架构章节

### 55. Validation-in-the-Loop 与持续质量门禁（P1）
- **来源**：2026-04-03 scan 发现
- **知识沉淀**：待创建 `memory/knowledge/agent-design/validation-in-the-loop-quality-gates-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：从"生成后验证"到"生成中持续验证"的范式转变。与 SlopCodeBench 揭示的退化问题对应——Validation-in-the-Loop 是工程解决方案。直接影响我们 go 命令创建子智能体时的验证点设计。
- **关键问题**：
  - 在 Skill 创建流程中，哪些步骤适合嵌入即时验证（而非等到最终检查清单）？
  - 架构合规性检查、lint、单元测试执行——哪些可以在生成阶段运行？
  - 与创建规范检查清单的关系——是否应该将部分检查前移？
  - Embedded Validation 的 token 开销和延迟影响？
- **后续**：直接应用到 go 命令的创建流程优化

### 56. Model Tiering 与任务级模型路由策略（P2）
- **来源**：2026-04-03 scan 发现
- **知识沉淀**：待创建 `memory/knowledge/agent-design/model-tiering-task-routing-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：生产系统中路由/分诊用廉价快速模型，复杂推理用重型模型。我们的 scheduler 目前固定使用 Opus 4.6，但 status/cron 等轻量命令可能不需要最重型模型。
- **关键问题**：
  - scheduler 的 YAML 配置是否支持 per-command model 指定？
  - 哪些命令适合轻量模型？（status、cron > scan > learn、go）
  - Model tiering 的成本节约预估？
  - 如何在不牺牲质量的前提下降级模型？
- **后续**：可能影响 scheduler 配置设计和 evo-skills-maintainer 的功能

### 57. A-Evolve — Git-Native Agent Evolution（P1）
- **来源**：2026-04-04 plan 搜索发现
- **知识沉淀**：待创建 `memory/knowledge/agent-design/a-evolve-git-native-evolution-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：A-Evolve 将 Agent 进化视为 CI/CD 过程，五阶段循环（Solve→Observe→Evolve→Gate→Reload），每个变异作为 Git 标签版本化（evo-1, evo-2），支持回滚和审计。核心创新是"Workspace-as-Code"——Agent 直接编辑工作区文件（逻辑、工具、manifest.yaml），而非仅调整 prompt。
- **关键问题**：
  - Git-native 版本化变异与我们的 evolution-log.md（文本日志）相比，结构化程度差距有多大？
  - 五阶段循环（Solve→Observe→Evolve→Gate→Reload）如何映射到我们的命令体系？
  - "Evaluation Gate"（严格验证后才接受新变异）对我们的 review 命令有什么启发？
  - 是否需要为子智能体的 SKILL.md 变更引入 Git 标签版本化？
- **后续**：可能影响 evolution-log.md 格式升级和 review 命令验证机制

### 58. Agent0 — Co-Evolutionary Dual-Agent Self-Improvement（P1）
- **来源**：2026-04-04 plan 搜索发现（ICLR 2026 Workshop on Recursive Self-Improvement）
- **知识沉淀**：待创建 `memory/knowledge/agent-design/agent0-co-evolutionary-dual-agent-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：Agent0 用 Curriculum Agent（教师）+ Executor Agent（学生）的双智能体架构实现"data-free"自进化。教师设计挑战任务→学生执行→教师学习学生缺什么→调整课程。关键贡献是解决了先前自我改进 Agent 的 mode collapse 和 degenerate curricula 问题。
- **关键问题**：
  - "任务生成与执行分离"的模式与我们的 learn/scan（发现知识差距）+ go（执行任务）是否存在映射？
  - Curriculum Agent 的"自适应课程"机制如何启发我们的 learning-plan 动态调整？
  - Mode collapse 防护机制对我们的进化模型有什么参考价值？
  - 能否让 review 命令扮演 Curriculum Agent 的角色——分析执行轨迹，识别薄弱环节，推荐学习方向？
- **后续**：可能影响 review 命令的"失败诊断"维度设计和 learning-plan 的自动调整机制

### 59. Contextual Drag — 错��记忆污染与 Clean History 管理（P1）
- **来源**：2026-04-04 plan 搜索发现（2026 Agent 研究热点）
- **知识沉淀**：待创建 `memory/knowledge/agent-design/contextual-drag-clean-history-2026.md`
- **学习次数**：0
- **状态**：待学习
- **为什么重要**：当 Agent 从过去错误/失败实验的记忆中学习时，错误模式会"污染"未来推理（Contextual Drag）。这是一个已被验证的系统性问题，现代框架开始强调"clean history management"。与我们高度相关——knowledge/ 下的知识文件如果包含早期错误理解，后续学习可能被误导。
- **关键问题**：
  - 我们的 knowledge/ 文件中是否存在 Contextual Drag 风险？（早期学习的浅层理解是否会误导深度学习）
  - execution.log 中的失败记录如何"clean"才能避免错误模式复制？
  - "Clean History"管理策略有哪些？标记过时/错误知识、版本化知识更新、隔离失败案例？
  - 与 #45 知识沉淀质量约束体系的关系——是否需要增加"错误知识标记与隔离"维度？
- **后续**：直接应用到 knowledge/ 目录管理策略和 review 命令的知识库健康扫描

## 统计

- **总学习项目**：60 项（合并重复后实际 58 项）
- **待学习**：17 项（P0: 0, P1: 10, P2: 7）
- **已完成首轮**：35 项
- **已完成深度研究**：6 项
- **知识文件总数**：43 个（agent-design/: 35, frameworks/: 8）
