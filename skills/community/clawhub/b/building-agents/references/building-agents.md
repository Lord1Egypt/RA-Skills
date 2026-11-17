# A Practical Guide to Building Agents — distilled

来源：OpenAI《A Practical Guide to Building Agents》。本文件把它重写为**可执行的程序化知识**：决策规则、反模式、模板、心智模型。目标是让一个 agent 照着它就能设计出可靠的 LLM Agent，而不必重读原书。

---

## Methodology（心智模型）

- **Agent = LLM 控制工作流执行 + Tools + Instructions + Guardrails**。它能自主完成多步任务；简单 chatbot、单轮 LLM、情感分类器**不是** agent——它们不用 LLM 控制流程。
- **先判断"要不要建"**：只有当传统确定性 / 规则方法搞不定时才上 agent。Agent 的价值在模糊、复杂、非结构化、规则难维护的场景。
- **渐进式演进**：从 single agent + 工具开始，只在必要时演化到 multi-agent。不要一上来就搞全自主复杂架构。
- **Guardrails 是分层防御**：单个 guardrail 不够，多个专用 guardrail 组合才 resilient。它必须和认证授权、访问控制、标准软件安全配合，不是替代。

---

## Core procedures

### 1. 决策：该不该建 Agent

决策规则（按顺序判断）：

- **IF** 工作流需要微妙判断 / 例外处理 / 上下文推理（传统规则引擎像清单、agent 像老练调查员）→ **考虑 agent**
- **IF** 系统因庞大规则集变得难维护、更新成本高 / 易错 → **考虑 agent**
- **IF** 重度依赖非结构化数据或自然语言（读文档、对话式交互）→ **考虑 agent**
- **ELSE** → 用确定性方案（规则 / 脚本）即可，**不要上 agent**

建之前的验证清单：

- [ ] 用例明确属于上面三类之一
- [ ] 否则：确定性方案足够 → 不选 agent（避免过度工程）

反模式：

- 为"看起来高级"而建 agent，实际只是单轮分类 → 用一次 LLM 调用就够了。
- 把简单 chatbot / 情感分类器当成 agent（它们不控制工作流执行）。

### 2. Agent 三组件（foundations）

每个 agent 由三件构成：

- **Model**：驱动推理与决策的 LLM。
- **Tools**：外部函数 / API，让 agent 取上下文、采取行动。Agent 与 Tool 是 many-to-many 关系。
- **Instructions**：明确的行为准则与边界（含 guardrails）。

### 3. 选型模型

程序：

1. 用**最强模型**给每个任务建原型，先建立性能基线（配 evals）。
2. 逐步换成更小 / 更快模型，测是否仍达标。
3. 优化成本与延迟：在达标前提下用大模型换小模型。

原则：不是每个任务都要最聪明模型。检索 / 意图分类用小模型；退款审批等难任务用强模型。

### 4. 设计工具

三类工具：

| 类型 | 作用 | 例子 |
|---|---|---|
| **Data** | 检索执行工作流所需的上下文 / 信息 | 查交易库 / CRM、读 PDF、搜 web |
| **Action** | 与系统交互、采取行动 | 发邮件 / 短信、更新记录、转人工 |
| **Orchestration** | agent 本身作为其他 agent 的工具 | refund agent、research agent |

规范：

- 每个工具**标准化定义**（name、参数、清晰 description）。
- 文档化、测试、可复用 → 提升可发现性、简化版本管理、避免重复定义。
- 工具数量变多 → 考虑拆到多个 agent（见 §6）。

反模式：

- 工具命名 / 描述含糊 → agent 选错工具。
- 10 个**重叠**工具比 15 个**清晰区分**的工具更糟。仅靠命名 / 描述无法提升时，用多 agent。

### 5. 写 Instructions

最佳实践：

- **用现有文档**：SOP、支持脚本、政策文档 → 生成 LLM 友好的 routines（客服 routine 可粗略映射到知识库单篇）。
- **拆小步骤**：从稠密资源拆成更小、更清晰的步骤，减少歧义。
- **明确动作**：每步对应具体动作或输出（连用户面对的措辞都写清），减少解释空间。
- **捕获边界情况**：用户给不全信息、问意外问题 → 用条件分支 / 替代步骤处理。
- 可用 o1 / o3-mini 等强模型从现有文档**自动生成 instructions**（给一个"把帮助中心文档转成无歧义编号指令"的 prompt 模板即可）。

### 6. 编排模式（Orchestration）

两类，按需选择：

**A. Single-agent（单智能体）**
- 一个模型 + 工具 + 指令，在 **run loop** 中执行，直到 exit condition：final-output tool 被调用 / 模型返回无 tool call / error / 达到最大轮数。
- 管理复杂度：用 **prompt templates**（单一灵活基础 prompt + 政策变量），而非维护一堆独立 prompt。新用例更新变量即可，不重写流程。

**B. Multi-agent（多智能体）**
- 工作流分布到多个协调的 agent。可用图建模：节点 = agent。
- **Manager pattern（agent as tool）**：中央 manager 通过 tool calls 协调多个 specialized agents。适合"只需一个 agent 控制执行 + 接触用户"。子 agent 用 `.as_tool()` 暴露。
- **Decentralized pattern（handoff）**：agent 间**单向**转移控制权 + 对话状态。handoff 在 SDK 里是一种 tool。适合不需中央控制、专业 agent 完全接管（如对话分诊）。可选给第二 agent 配 handoff 回原 agent。
- 声明式图（预定义每个分支 / 循环 / 条件）在动态复杂工作流中迅速笨重、要学 DSL → 偏好 **code-first**（如 Agents SDK 直接用编程语言表达流程）。

**何时拆多代理（guidelines）**：

- 复杂逻辑：prompt 含大量 if-then-else，模板难扩展 → 按逻辑段分 agent。
- Tool overload：工具相似 / 重叠，仅靠命名 / 描述 / 详细参数无法提升性能 → 多 agent。
- 总原则：**最大化单 agent 能力优先**；多 agent 增加复杂度与开销，往往单 agent + 工具就够。

反模式：

- 一上来就建全自主复杂多 agent 架构（客户通常用渐进式更成功）。
- 在动态工作流里硬用声明式图。

### 7. Guardrails（分层防御）

心智：单个 guardrail 不太可能提供足够保护；多个专用 guardrail 组合才 resilient。**必须**与健壮的认证授权、严格访问控制、标准软件安全配合。

类型：

| 类型 | 作用 |
|---|---|
| **Relevance classifier** | 标记离题查询，确保响应在预期范围内 |
| **Safety classifier** | 检测 jailbreak / prompt injection（试图窃取系统指令） |
| **PII filter** | 防止输出暴露个人身份信息 |
| **Moderation** | 标记仇恨 / 骚扰 / 暴力等有害输入 |
| **Tool safeguards** | 给每个工具评风险 low / medium / high（只读 vs 写、可逆性、所需权限、财务影响），触发自动动作（高风险前暂停检查 / 转人工） |

构建 heuristic：

1. 专注**数据隐私 + 内容安全**。
2. 基于真实边界情况 / 失败，**逐步加**新 guardrail。
3. 优化**安全与 UX 平衡**，随 agent 演化调整。

实现手段：

- **Rules-based protections**：blocklist、输入长度限制、regex 过滤已知威胁（违禁词、SQL 注入）。
- **Output validation**：通过 prompt 工程 + 内容检查确保输出对齐品牌价值。
- **Optimistic execution**（默认）：主 agent 主动生成输出，guardrail **并发**运行，违例才抛异常。
- guardrail 可实现为 **function 或 agent**（jailbreak 防护、相关性校验、关键词过滤、blocklist、安全分类）。

**Human intervention（关键 safeguard）**：

- 让 agent 在无法完成任务时优雅交还控制权（客服 → 转人工；编码 agent → 交还用户）。
- 早期部署尤其重要：发现失败、暴露 edge cases、建立 eval cycle。
- 两个主要触发：
  1. **超失败阈值**：设重试 / 动作次数上限，超限（如多次仍不理解用户意图）→ 转人工。
  2. **高风险动作**：敏感 / 不可逆 / 高 stake（取消订单、授权大额退款、付款）→ 在可靠性建立前需人工 oversight。

---

## Quick reference

**该不该建 agent？** 判定表：

| 信号 | 决策 |
|---|---|
| 需要微妙判断 / 例外 / 上下文推理 | 建 agent |
| 规则集庞大难维护 | 建 agent |
| 重度非结构化数据 / 自然语言 | 建 agent |
| 以上都不是 | 确定性方案 |

**工具三类**：Data（取上下文）、Action（采取行动）、Orchestration（agent 当工具）。

**编排选型**：单 agent（+prompt 模板） → 仅在复杂逻辑 / 工具过载时拆 Manager（中央协调）或 Decentralized（handoff）。

**Guardrail 类型**：Relevance / Safety / PII / Moderation / Tool safeguards；手段 = rules-based + output validation + optimistic execution + human-in-the-loop。

---

## Source mapping（原书章节 → 本知识包）

| 原书章节 | 本文件 |
|---|---|
| Introduction | Methodology |
| What is an agent? | §2 三组件定义、agent vs 非 agent |
| When should you build an agent? | §1 决策规则 |
| Agent design foundations | §2 三组件 |
| Selecting your models | §3 选型 |
| Defining tools | §4 工具设计 |
| Configuring instructions | §5 instructions |
| Orchestration | §6 概览 |
| Single-agent systems | §6-A |
| Multi-agent systems | §6-B（Manager / Decentralized） |
| Guardrails | §7 心智 + 类型 |
| Types of guardrails | §7 类型表 |
| Building guardrails | §7 构建 heuristic + human intervention |
| Conclusion | Methodology（渐进式、迭代） |
