# Evidence Association Pitfalls — AI Agent 关键信息关联缺失错误模式库

[中文](#中文) | [English](#english)

---

## 中文

### 这是什么

一个聚焦单一高危错误模式的 AI Agent 行为校准 skill：**关键信息关联缺失（Evidence Association Failure）**——Agent 手握足以推导正确结论的信息，却未建立关联，转而套用外部模板、惯性标签或默认常识。

它与"检索失败"（信息在档案没去读）和"幻觉"（信息不存在却编造）不同：**信息就在上下文里，Agent 甚至读过它，但没让证据参与推理。** 这是最隐蔽的一类——事后检查时"看起来引用了上下文"，实际结论与证据完全脱节。

### 为什么值得单独一个 skill

本模式源自真实 Agent 对话中被用户当场抓包的连环错误（已脱敏）。它有两个被低估的特性：

1. **长对话自强化**：早期贴错的标签会随对话越用越顺，用户不纠正就一路错到底，且后续所有建议都在歪掉的前提上展开
2. **证据在场性伪装**：因为错误发生时证据确实在场，常规的"检查是否引用上下文"防不住它——需要的是"检查证据与结论是否匹配"

### 内容

- 与近邻错误（未调档 / 关联缺失 / 幻觉）的**区分谱系表**
- **4 类高频触发场景**（含脱敏案例）：设计行为与外部模板冲突 / 画像硬约束未过滤推荐 / 名词激活错误关联域 / 单点状态推因果
- **输出前检测信号清单**（5 项自查）
- **5 条可执行预防规则**
- 正误对照最小样本

### 快速预览：一条核心规则

> **用户的实际设计行为 > 用户的言语 > Agent 的外部知识。** 三层证据冲突时，优先级不可颠倒——如果你的结论依据的是"行业里通常如此"，而用户刚做的设计指向别处，错的是你的结论。

### 适用对象

- AI Agent 的系统提示词设计者（反模式参考）
- Agent 对话质量复盘与错误归档
- 多项目语境下工作的 AI 助手（串线高发区）
- 任何想让 AI "把手里证据用起来"的用户

详见 [SKILL.md](SKILL.md)。

---

## English

### What is this

An AI Agent behavior-calibration skill focused on a single high-risk failure mode: **Evidence Association Failure** — the agent holds information sufficient to derive the correct conclusion, but never connects evidence to conclusion, and instead falls back on external templates, habitual labels, or default assumptions.

Distinct from retrieval failure (context existed but was never read) and hallucination (fabrication): **the evidence is right there in the conversation — the agent may have even quoted it — but never let it participate in reasoning.** This is the most insidious variant: a post-hoc check sees "context was referenced," while the conclusion is actually detached from every piece of evidence.

### Why a dedicated skill

Derived from a chain of real errors caught by the user in a live Agent session (anonymized). Two underestimated properties:

1. **Self-reinforcing in long conversations**: a wrong label applied early gets reused more smoothly over time; without user correction, every subsequent suggestion is built on the warped premise
2. **Evidence-presence disguise**: since the evidence IS present when the error occurs, "check if context was cited" won't catch it — you need "check if evidence matches conclusion"

### Contents

- A **differentiation table** vs. neighboring failure modes (unread context / association failure / hallucination)
- **4 high-frequency trigger scenarios** (anonymized cases): design-behavior vs. external-template conflict / hard-constraint filtering missed / noun-activated wrong domain / causal story from a single snapshot
- **Pre-output detection checklist** (5 items)
- **5 actionable prevention rules**
- A minimal correct/incorrect comparison

### Quick preview: one core rule

> **The user's actual design behavior > the user's words > the agent's external knowledge.** When these three conflict, priority must not be inverted — if your conclusion relies on "this is how it's usually done in the industry" while the user's latest design points elsewhere, it's your conclusion that's wrong.

See [SKILL.md](SKILL.md) for the full reference.

---

## License

MIT

## AI Usage Disclosure

- 本库由 AI（Claude/三月七）起草、维护者审核定稿；案例源自真实 AI Agent 对话中的错误，已全量脱敏（项目名、地点、平台、个人信息均已泛化）
- This library was drafted by an AI assistant and reviewed/approved by the maintainer. Cases are derived from real AI agent conversations, fully anonymized (project names, locations, platforms, and personal information have been generalized).
