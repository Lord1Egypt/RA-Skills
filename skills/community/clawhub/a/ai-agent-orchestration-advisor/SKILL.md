---
name: AI Agent Orchestration Advisor
description: >
  Scope: framework comparison, architecture design, starter-code scaffolds and evaluation design for multi-agent systems; it does not run, install, or deploy any framework.  AI-powered multi-agent framework comparison and selection assistant — analyze use cases,
  compare LangGraph/CrewAI/OpenAI Agents SDK/Claude Agent SDK, generate architecture
  recommendations and starter code. Keywords: multi-agent, agent orchestration, LangGraph,
  CrewAI, OpenAI Agents SDK, Claude Agent SDK, Strands Agents, AutoGen, agent framework
  comparison, AI agent architecture, multi-agent system design, agent SDK, 多智能体,
  智能体编排, 框架对比, 智能体架构.
version: "3.0.3"
---

# AI Agent Orchestration Advisor / 多智能体编排选型顾问

> Your expert co-pilot for designing, selecting, and implementing multi-agent AI systems.
> 面向多智能体系统的选型、架构设计与落地实施：从需求澄清到框架对比、架构拓扑、起步代码、评测护栏与成本测算。

## What This Skill Does

In 2026, the agentic AI ecosystem exploded — LangGraph, CrewAI, AutoGen/AG2, OpenAI Agents SDK, Claude Agent SDK, and Strands Agents all compete for developer mindshare. Picking the wrong framework wastes weeks. This skill helps you:

- **Choose the right framework** for your specific use case (workflow complexity, state management, team size, hosting requirements)
- **Generate architecture diagrams** and data flow specs for multi-agent systems
- **Produce starter code** scaffolds (Python) for the chosen framework
- **Analyze trade-offs** across orchestration patterns (hierarchical, sequential, parallel, event-driven)
- **Design evaluation and guardrails** before go-live, including human-review checkpoints
- **Estimate cost and capacity** per run and per month
- **Debug and optimize** existing multi-agent implementations

## Trigger Words / 触发词

**English Triggers:** multi-agent framework comparison, agent orchestration design, LangGraph vs CrewAI, agent architecture topology, agent evaluation and guardrails, agent cost estimation, agent state persistence debugging

**English Non-Triggers:** single prompt writing, general chatbot building, model fine-tuning, RAG pipeline basics unrelated to agents, web scraping scripts, generic Python debugging

**中文触发词（须落在多智能体选型或设计任务上才触发）：** 多智能体框架怎么选 / 智能体编排模式有哪些 / 有状态智能体怎么做断点恢复 / 多智能体评测指标怎么定 / 智能体护栏怎么设计 / 多智能体成本怎么测算 / 智能体循环失控怎么处理

**不触发清单：** 单条提示词优化、通用大模型问答、模型微调与训练、普通脚本编写、纯项目管理咨询

**路由判定三步**：① 任务是否涉及两个及以上 Agent 的协作、编排或框架选型？② 是否需要输出架构、代码脚手架、评测或成本结论？③ 前两步均为是才启用本技能；单 Agent 场景转提示词工程或应用开发类技能。

## Target Users / 适用人群


- AI engineers building production agent systems
- Data scientists exploring agentic automation
- Product managers scoping agent-based features
- Developers migrating from single LLM to multi-agent pipelines
- **金融行业科技与数据团队**：需同时满足业务交付与合规留痕要求

---

## Ecosystem & Compliance Updates [2026-11-14] / 生态与合规动态

| 类型 | 内容摘要 | 对选型的影响 | 落地动作 | 优先级 |
|-----|---------|-----------|---------|-------|
| 框架成熟度 | LangGraph 状态机路线趋于稳定：状态持久化/长期记忆/错误恢复成为基线能力，企业级部署支持容器编排扩缩容 | 复杂有状态工作流首选评估对象 | 以"状态恢复是否可验证"作为 POC 验收项 | 高 |
| 多智能体协作 | CrewAI 路线强化角色化协作与并行任务编排，连接器生态扩张 | 角色清晰、流程线性的场景上手成本低 | 先用 2-3 个角色做最小闭环 | 高 |
| SDK 竞争 | Claude Agent SDK / OpenAI Agents SDK 在工具调用与上下文利用上各有侧重 | 与既有模型生态绑定程度决定迁移成本 | 以"模型可替换性"评估锁定风险 | 高 |
| 协议生态 | MCP 生态持续扩张，企业内部 MCP 注册表逐步成为基础设施 | 工具接入标准化，减少定制胶水代码 | 建立内部工具注册与权限清单 | 中 |
| 互操作协议 | Agent 间互操作协议（如 A2A 方向）推进，跨系统协作成为议题 | 跨部门/跨厂商协作场景需预留适配层 | 关键接口做抽象层，避免直连 | 中 |
| 长上下文 | 主流模型上下文窗口差异显著，长文档场景成本差异被放大 | 金融长文档场景需按"分片 + 检索"而非全量投喂 | 以 10 万字符文档做成本对照测试 | 中 |
| AI 治理 | 金融机构 AI 应用需满足安全开发与合规使用要求，涉及场景清单、数据来源与人工复核 | Agent 系统需自带留痕与复核环节 | 上线清单中加入治理条目 | 高 |
| 可观测性 | 评测与追踪工具成为生产必备 | 无追踪能力的框架运维成本高 | 选型时把追踪能力纳入打分 | 中 |
| 上下文工程 | 上下文压缩、剪枝与长期记忆分层成为降本主线，不再是简单扩大窗口 | 长任务成本结构改变 | 把「每步上下文净增量」纳入成本测算项 | 高 |
| 沙箱与隔离 | 代码执行类工具普遍要求沙箱化与资源限额 | 涉及代码执行的 Agent 需额外隔离设计 | 工具清单中标注哪些必须在沙箱内运行 | 高 |

> **数据截止**: 2026-11-14 | 来源：各框架官方文档与公开版本说明、协议公开资料、行业公开信息
> **声明**: 以上为生态观察与技术选型参考，框架版本与能力请以官方最新发布为准

**动态解读示例（两类高频场景）**

- **场景A｜框架锁定风险被低估**：团队为快速交付直接把业务逻辑写入某 SDK 的专有抽象层，半年后需要更换模型供应商 → 迁移成本约等于重写。**改进动作**：把"模型调用、工具定义、记忆存储"三类接口做薄抽象层；POC 阶段就验证一次模型替换（换供应商跑同一套评测集）。
- **场景B｜缺失追踪导致问题无法定位**：多智能体跑出错误结论，但未记录中间步骤与工具调用参数 → 无法复盘是检索错、工具错还是生成错。**改进动作**：选型时将"每步输入输出可导出、可回放"列为硬性要求，并在 POC 中导出一次完整调用链。

- **场景C｜并行分支的结果合并无一致性处理**：三个子 Agent 并行取数后直接拼接输出，未定义冲突消解规则 → 同一问题两次运行结果不一致，且无法判断哪个对。**改进动作**：并行分支后固定一个「汇总与冲突消解」节点，明确冲突时的优先级（可信来源优先 / 时间戳优先 / 转人工），并在评测集中加入一致性用例（同输入跑 10 次比对）。

---

## Data Minimization & Execution Boundary / 数据最小化与执行边界

**数据最小化前置声明（使用本技能前请先执行）**

1. 描述需求时不要粘贴真实业务数据、客户信息、内部接口地址与账号口令；用字段化描述替代（如「一批合同文本，含甲乙双方与金额」）。
2. 起步代码中的 API Key、数据库连接串一律使用占位符（如 `os.environ["..."]`），不得写入明文凭据。
3. 需要评估真实数据时，先做脱敏与抽样，且样本不得离开机构内网。
4. 本技能不安装、不运行、不部署任何框架；不访问用户的代码仓库、终端或云端环境；不发起任何外部网络调用。
5. 生成的代码脚手架与配置如需落盘或提交，须先预览全文、确认无凭据与内网地址残留，再由责任人按机构变更流程办理。

**代码块性质与执行边界**

| 内容 | 性质 | 谁来执行 |
|------|------|---------|
| Step 4 的 CrewAI 示例 | 可运行脚手架，需在用户本地安装依赖后执行 | 使用者在自己的环境中运行，本技能不执行 |
| Step 4.1 的 LangGraph 骨架 | 片段示例，省略了图构建与检查点配置 | 使用者补全后运行，本技能不执行 |
| 框架对比表中的能力标注 | 生态观察结论，随版本变化 | 使用者以官方文档复核后采用 |
| 部署检查清单 | 上线前的自查项 | 使用者的工程与合规团队 |

**硬边界**：不执行代码、不安装依赖、不读写用户文件系统、不发起网络请求、不访问凭据、不代为部署上线。


## Step 1 — Understand the Use Case

Ask the user to describe:

- The task or workflow to automate (e.g., "research + summarize + post")
- Number of distinct roles/agents needed
- State persistence requirements (ephemeral vs. persistent)
- Hosting preference (cloud / local / serverless)
- Team's programming experience

### 1.1 Requirement Intake Table / 需求采集表

| 维度 | 关键问题 | 为什么重要 | 常见误判 | 判定依据（可用于追问） |
|-----|---------|-----------|---------|---|
| 任务形态 | 线性流程、分支决策还是开放探索？ | 决定编排模式（顺序/图/事件驱动） | 把线性流程做成多智能体 | 能否画出只有单向边的流程图？能则偏线性 |
| 角色数量 | 真正需要几个不同职责？ | 角色越多，通信成本与失败点越多 | 为"看起来强大"堆角色 | 两个角色职责是否可被同一个人完成？能则合并 |
| 状态需求 | 是否需要跨会话记忆与断点恢复？ | 决定是否必须有持久化检查点 | 用外部数据库硬凑 | 中断后是否需要从断点继续？需要则必须持久化 |
| 延迟预算 | 单次任务可接受多少秒？ | 多跳调用会线性放大延迟 | 忽略并行化的可行性 | 用户会在页面前等待还是异步取结果？ |
| 成本上限 | 单次任务可接受成本？ | 角色数与上下文窗口直接放大成本 | 按"每个 Token 单价"估算而非按任务 | 单任务成本是否高于人工成本的 30%？ |
| 部署环境 | 公有云、私有化还是一体机？ | 部分框架/服务在私有化下受限 | 忽略内部网络与数据出域限制 | 是否有数据不出内网的硬性约束？ |
| 团队技能 | 团队熟悉 Python 异步与状态管理吗？ | 决定学习曲线是否可承受 | 低估调试成本 | 团队能否独立排查异步死锁与状态污染？ |
| 合规要求 | 是否需要留痕、复核、可解释？ | 金融场景为硬性要求 | 上线前才补 | 是否会被审计或监管调阅？ |

---

## Step 2 — Framework Shortlist & Comparison

### 2.1 Comparison Table / 框架对比

| Framework | Best For | State Mgmt | Learning Curve | Hosting | Observability | 成本模型 | 锁定风险 |
|-----------|----------|------------|----------------|---------|--------------|--------|---|
| LangGraph | Complex stateful workflows | ✅ Built-in | Medium | Any | 强（图级追踪） | 按节点调用计费 | 图抽象与框架绑定，迁移需重写节点 |
| CrewAI | Role-based team simulations | Partial | Low | Any | 中 | 按角色任务计费 | 角色与任务模型绑定，深度定制时受限 |
| AutoGen/AG2 | Conversational agent loops | External | Medium | Any | 中 | 按轮次计费 | 会话循环模型绑定，转向图结构成本较高 |
| OpenAI Agents SDK | OpenAI ecosystem, handoffs | Built-in | Low | Cloud-first | 中 | 按调用计费 | 与厂商模型能力强绑定，换供应商需改造 |
| Claude Agent SDK | Anthropic native, tool use | Built-in | Low | Cloud-first | 中 | 按调用计费 | 同上，且工具协议为厂商私有 |
| Strands Agents | AWS/Bedrock integration | External | Medium | AWS | 依赖云侧 | 按云服务计费 | 与云服务强绑定，私有化受限 |
| LlamaIndex Workflows | 检索增强类流程 | Built-in | Low | Any | 中 | 按调用计费 | 检索组件绑定，非检索类流程优势不明显 |
| Semantic Kernel | .NET/多语言企业栈 | External | Medium | Any | 中 | 按调用计费 | 企业栈绑定，生态插件相对少 |
| 低代码平台（Dify/Coze 类） | 内部工具、快速验证 | Built-in | Very Low | SaaS/私有 | 弱至中 | 按订阅计费 | 平台绑定，复杂逻辑与私有化受限 |

### 2.2 Selection Decision Table / 选型决策表

| 情形 | 首选 | 次选 | 理由 | POC 验收项 |
|-----|------|------|------|---|
| 有状态、需断点恢复的长流程 | LangGraph | LlamaIndex Workflows | 图结构与检查点是核心诉求 | 断电/中断后能从检查点恢复并继续 |
| 角色清晰、线性协作 | CrewAI | AutoGen/AG2 | 上手快，角色定义直观 | 两角色最小闭环一次跑通且可回放 |
| 需要与既有模型生态深度绑定 | 对应厂商 SDK | LangGraph | 官方 SDK 的工具与回退机制更完整 | 换一个模型供应商跑同一评测集结果不劣化 |
| 强检索依赖（知识库问答） | LlamaIndex Workflows | LangGraph | 检索组件成熟 | 同题 10 次检索命中一致 |
| 企业 .NET 技术栈 | Semantic Kernel | LangGraph | 与既有服务栈一致 | 与既有 .NET 服务互通，无胶水层堆积 |
| 快速验证业务想法 | 低代码平台 | CrewAI | 一周内可出可用原型 | 一周内产出可被业务方使用的原型 |
| 私有化 + 强合规留痕 | LangGraph | 自研轻量状态机 | 追踪与持久化可完全自控 | 调用链可完整导出至内网存储 |

> **规则**：先用"流程是否有状态 + 是否需要检索 + 部署限制"三个问题筛掉大部分选项，再在剩余的 2-3 个里做 POC 对比。

---

## Step 3 — Architecture Recommendation

Output a recommended architecture including:

- Agent topology (who calls whom)
- Tool assignments per agent
- Memory / state strategy
- Human-in-the-loop checkpoints
- Error handling & fallback patterns

### 3.1 Orchestration Patterns / 编排模式

| 模式 | 适用场景 | 优点 | 风险 | 典型实现 | 成本特征 |
|-----|---------|------|------|---------|---|
| 顺序（Sequential） | 步骤确定的流水线 | 易调试、成本可预测 | 缺乏动态调整能力 | CrewAI Process.sequential | 成本随步骤线性增长，最可预测 |
| 层级（Hierarchical） | 需要主管分配与汇总 | 复杂任务可分工 | 主管节点易成瓶颈 | 主管 Agent + 子 Agent | 主管节点上下文膨胀，成本集中在汇总层 |
| 并行（Parallel） | 多源独立取数/多方案比较 | 降低总延迟 | 结果合并需一致性处理 | 并发任务 + 汇总节点 | 总成本不一定下降，但墙钟时间显著下降 |
| 事件驱动（Event-driven） | 长时任务、需外部触发 | 解耦、可扩展 | 状态追踪复杂 | 队列 + 状态机 | 空闲等待不计费，但长驻状态有存储开销 |
| 评审循环（Critic loop） | 质量要求高的产出 | 自我纠错 | 循环失控导致成本飙升 | 生成 + 评审双角色 | 成本随轮次倍增，必须设上限 |

**拓扑示例（层级 + 评审循环）**

```
Coordinator
 ├── Retriever Agent   → 工具：知识库检索
 ├── Analyst Agent     → 工具：结构化计算
 └── Writer Agent      → 工具：文档生成
        ↑
   Critic Agent ── 不通过则回退到对应节点（限 2 轮）
```

### 3.2 Human-in-the-Loop Checkpoints / 人工复核卡点

| 卡点 | 触发条件 | 人工动作 | 留痕要求 | 未设卡点的后果 |
|-----|---------|---------|---------|---|
| 外发前 | 产出将对外使用 | 复核事实与表述 | 复核人、时间、版本 | 错误表述直接对外，追溯时无法定位复核人 |
| 高金额/高风险决策 | 涉及资金或风险判断 | 双人复核 | 双人签字或系统记录 | 单人决策错误无第二道防线，且责任不清 |
| 低置信输出 | 置信度低于阈值 | 转人工处理 | 标注不确定点 | 低置信结论被当作确定结论使用 |
| 循环失控 | 评审循环超过预设轮数 | 中止并转人工 | 保留循环记录 | 循环空转持续消耗预算，且产出不可用 |

---

## Step 4 — Starter Code Generation

Generate a complete, runnable Python scaffold:

```python
# Example: CrewAI research + report pipeline
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in {topic}",
    backstory="You are an expert researcher...",
    tools=[search_tool],
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Craft insightful, accurate reports from research",
    backstory="You transform raw research into executive summaries...",
    verbose=True
)

research_task = Task(
    description="Research {topic} thoroughly...",
    agent=researcher,
    expected_output="Bullet-point research findings"
)

write_task = Task(
    description="Write a 500-word report on the research findings",
    agent=writer,
    expected_output="Polished report with sections"
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "agentic AI in 2026"})
```

### 4.1 Stateful Skeleton (LangGraph style) / 有状态骨架

```python
from typing import TypedDict

class State(TypedDict):
    query: str
    findings: list
    draft: str
    review_passed: bool
    rounds: int

def route_after_review(state: State) -> str:
    """评审后的路由：通过则结束，未通过且轮次未超限则回退"""
    if state["review_passed"]:
        return "end"
    if state["rounds"] >= 2:
        return "human_review"      # 循环超限 → 转人工，避免无限循环
    return "revise"

# 关键点：
# 1) 检查点持久化，支持中断恢复
# 2) 循环轮次上限，防止成本失控
# 3) 低置信输出走人工复核分支
```

### 4.2 交付物清单 / Deliverables Checklist

- [ ] 架构拓扑图（节点、边、条件路由）
- [ ] 每个 Agent 的职责边界与工具清单
- [ ] 状态结构定义与持久化方案
- [ ] 评审与回退规则（含轮次上限）
- [ ] 人工复核卡点清单
- [ ] 评测集与验收标准


**模块4 示例（两条）**

- **示例A｜四角色流程的骨架拆解**：需求为「自动生成行业简报，需可回溯、可复核」。骨架拆解：Retriever（工具：内网知识库检索，只读）+ Analyst（工具：结构化计算，无外部网络）+ Writer（工具：文档生成）+ Critic（无工具，仅评审）；状态结构含 `query / findings / draft / review_passed / rounds`；`route_after_review` 中 `rounds >= 2` 强制转 `human_review`；检查点持久化到内网库。**关键约束**：Critic 不通过时回退到对应节点而非从头重跑，避免重复计费。
- **示例B｜起步代码的三处必改项**：拿到 CrewAI 脚手架后必改：① `SerperDevTool`（外网检索）改为内网检索工具或明确列入数据出域审批；② API Key 改为从环境变量读取，禁止硬编码；③ `verbose=True` 的日志改为结构化落盘并脱敏，避免原始业务文本进入日志。未改完不上测试环境。

---

## Step 5 — Evaluation & Guardrails / 评测与护栏

### 5.1 Evaluation Dimensions / 评测维度

| 维度 | 指标示例 | 采集方式 | 参考门槛 | 不达标时的处理 |
|-----|---------|---------|---------|---|
| 任务完成率 | 端到端成功比例 | 评测集回放 | ≥85% | 定位失败最集中的节点，先砍角色再调提示 |
| 事实准确性 | 与可信来源一致的比例 | 抽样核对 | 关键字段 100% | 关键字段改走确定性抽取，不让模型自由生成 |
| 工具调用正确率 | 参数与调用对象正确比例 | 调用日志 | ≥95% | 给工具加参数校验与重试，必要时收窄工具描述 |
| 稳定性 | 重复运行结果一致性 | 同输入跑 10 次 | 结论一致 | 固定随机性来源（温度、检索 Top-K），再做对照 |
| 延迟 | 端到端耗时 | 埋点 | 符合延迟预算 | 把串行改并行，或降低单跳上下文 |
| 成本 | 单任务成本 | 用量统计 | 符合成本上限 | 先降上下文净增量，再谈降角色数 |
| 可回放性 | 调用链可导出比例 | 追踪系统 | 100% | 补齐追踪埋点后再上线，否则不具备投产条件 |

### 5.2 Guardrails / 护栏清单

| 护栏 | 实现方式 | 检查点 | 失效表现 |
|-----|---------|-------|---|
| 工具白名单 | 仅注册允许的工具 | 上线前审核 | 出现未注册工具被调用 |
| 输入输出过滤 | 敏感信息与不当内容拦截 | 每次调用 | 敏感字段出现在输出或日志中 |
| 循环上限 | 迭代轮次与总调用数上限 | 运行时 | 单任务调用数远超预算，账单异常 |
| 超时与熔断 | 单步与整体超时 | 运行时 | 任务长时间挂起占用资源 |
| 权限最小化 | 工具按最小权限授权 | 上线前 | 工具可访问超出职责范围的数据 |
| 数据出域控制 | 敏感数据不出内网 | 架构评审 | 内网数据出现在外部服务日志中 |
| 全链路留痕 | 输入、输出、参数、人工动作 | 100% | 事后无法复盘某次结论的生成过程 |

---

## Step 6 — Cost & Capacity Estimation / 成本与容量测算

| 项目 | 测算口径 | 示例（单任务） | 压缩手段 |
|-----|---------|-------------|---|
| 模型调用 | 各角色 Token 用量 × 单价 | 3 角色 × 8K Token | 减少角色数、降低每步上下文净增量 |
| 检索调用 | 检索次数 × 单次成本 | 5 次 | 检索结果先摘要再入上下文，控制 Top-K |
| 外部工具 | 第三方 API 调用次数 | 2 次 | 合并调用、加缓存，避免重复查询 |
| 延迟 | 串行跳数 × 单跳耗时 | 4 跳 × 3 秒 | 串行改并行，缩短关键路径 |
| 重试开销 | 预计重试率 | +15% | 先消除失败根因，再容忍重试 |

**示例测算**：一个"检索 + 分析 + 撰写 + 评审"四角色流程，单任务约 4 跳、合计约 3 万 Token；若以固定单价估算，可通过"降低角色数 + 并行取数 + 结果复用"把单任务成本压缩 30%-50%。**测算应基于实测用量，而非按单价线性外推。**

---

## Step 7 — Production Checklist / 生产检查清单

- [ ] Rate limiting & retry logic
- [ ] Observability (LangSmith / Weights & Biases / custom logging)
- [ ] Secrets management (never hardcode API keys)
- [ ] Cost estimation per run
- [ ] Human review gates for high-stakes outputs
- [ ] 状态持久化与中断恢复验证
- [ ] 循环轮次与总调用数上限
- [ ] 工具权限最小化与白名单
- [ ] 数据出域与脱敏策略
- [ ] 评测集与回归测试流程
- [ ] 版本管理与提示词变更记录
- [ ] 故障演练（工具失败、模型超时、返回格式异常）
- [ ] 上下文净增量监控（每步上下文增长是否失控）
- [ ] 代码执行类工具的沙箱与资源限额验证
- [ ] 日志脱敏检查（原始业务文本是否进入日志）
- [ ] 提示词与框架版本的变更记录可回溯到具体发布

## Example Interactions

**User:** "I need to build a system where one agent searches the web, another analyzes sentiment, and a third writes a report. Which framework should I use?"

**Skill response:** Recommends CrewAI for its role-based simplicity, provides a 3-agent architecture diagram, generates a complete scaffold with SerperDevTool + OpenAI, and provides a deployment checklist.

**User:** "I'm using LangGraph but my agents keep losing context between nodes. How do I fix state persistence?"

**Skill response:** Explains LangGraph's StateGraph checkpointing, shows how to add a PostgreSQL checkpointer, provides a code fix.

**User:** "我们的投研团队想做一个自动生成行业简报的多智能体系统，但必须可回溯、可人工复核。"

**Skill response:** 推荐"检索 → 分析 → 撰写 + 评审循环"的层级拓扑，给出状态结构与人工复核卡点表，明确要求每步调用链可导出、循环不超过 2 轮，并给出评测维度与门槛建议。

**User:** "多智能体系统上线后成本比预期高 3 倍，怎么排查？"

**Skill response:** 按"角色数 × 跳数 × 上下文长度 × 重试率"拆解，指出常见原因是评审循环无上限、检索结果全量投喂、以及角色冗余；给出三项压缩动作与验证方式。



**User:** "两个 Agent 并行取数后结果打架，同一问题两次跑出来的结论不一样，怎么办？"

**Skill response:** 判定为并行分支缺少汇总与冲突消解节点。给出：在并行分支后固定一个汇总节点，冲突时按「可信来源优先 → 时间戳优先 → 转人工」的优先级消解；评测集中加入一致性用例（同输入跑 10 次比对结论）；并把汇总节点的输入固定为结构化字段而非自由文本，降低合并歧义。

**User:** "我们要在私有化环境里跑多智能体，且监管会调阅每次结论的生成过程。"

**Skill response:** 优先选可完全自控追踪与持久化的方案（LangGraph 或自研轻量状态机），要求：检查点与调用链落内网存储、日志脱敏后留存、人工复核卡点在系统中留痕（复核人/时间/版本）、代码执行类工具进沙箱；同时把「调用链可导出比例 100%」列为上线硬门槛，并给出评测维度与门槛建议。

## Changelog / 版本变更

| 版本 | 日期 | 变更摘要 |
|------|------|---------|
| 3.0.2 | 2026-10-09 | 新增数据最小化前置声明与代码块性质/执行边界表（明确不安装/不运行/不部署框架）；收窄中英文触发词、补充非触发清单与路由判定三步；生态动态更新至2026-10-09并新增上下文工程、沙箱与隔离两条；全线表格新增列：判定依据、锁定风险、POC验收项、成本特征、未设卡点的后果、不达标时的处理、失效表现、压缩手段；Step4新增两条示例（四角色骨架拆解、起步代码三处必改项）；新增解读场景C（并行结果合并无一致性处理）；生产清单补4条；新增2组对话示例 |
| 3.0.1 | 2026-09-13 | 新增生态与合规动态、评测护栏与成本测算 |

---



## Notes & Constraints

- Always surface the **trade-offs**, not just the "winner" — different teams need different frameworks
- Code examples default to Python; mention JS/TS equivalents where available
- For enterprise requirements, flag SOC2 / data residency considerations
- Keep up with the rapidly evolving MCP (Model Context Protocol) and A2A protocol integrations
- Recommend starting simple: single agent → multi-agent only when genuinely needed
- 金融行业落地需额外关注：数据不出域、全链路留痕、人工复核卡点、循环与调用上限
- 框架版本与生态变化快，选型结论应标注评估日期并定期复核

## 本轮增量（2026-11-14）：复核维度与举例补充

> 本节为 2026-11-14 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Step 2 — Framework Shortlist & Comparison**：

- 对照表补「上下文隔离方式 / 版本锁定口径」两项，草稿只记录纸面对照结论，不代为安装或选型落地。
- 候选框架新增「官方文档最近更新日期」标注位，超期条目标为待核实，避免把历史资料当作当前能力。

**Step 5 — Evaluation & Guardrails / 评测与护栏**：

- 评测清单补「固定对照集 / 分层评分卡点」两项，明确为文档记录口径，由人员确认后再使用。
- 护栏说明新增「逐步校验：结构完整性、字段齐全性、数据新鲜度」三项的纸面核对顺序，不含运行指令。

### 新增复核维度表（2026-11-14）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 版本锁定口径 | 架构人员 + 复核人 | 官方版本说明 | 锁定方式、依赖边界、更新来源 | 中 | 选型草稿，落地由人员确认 |
| 评测对照集 | 评测人员 + 复核人 | 固定对照集 + 评分卡 | 覆盖分布、评分维度、回归对照 | 中 | 文档记录，不构成上线结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于多智能体方案选型与评测设计的方法论参考，输出为供具备相应资质人员复核的纸面设计材料；不安装框架、不运行示例代码、不部署系统、不代为接入数据。涉及生产部署、权限开通与外部服务接入的场景不适用，应转由相应技术系统与授权人员处理。

### 参考同类公开框架的补强（2026-11-14）

> 参考同类公开框架文档的思路补强：逐步校验（结构完整性 / 字段齐全性 / 数据新鲜度）、固定对照集与分层评分卡点、版本与依赖边界的纸面标注。仅吸收方法论结构，未引入任何具体命令、工具版本号或第三方资料原文。

### 时效性说明

- 本期时效性核查：**截至 2026-11-14**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
