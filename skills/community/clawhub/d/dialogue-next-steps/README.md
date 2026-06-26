# Dialogue Next Steps

[English](#english) | [中文](#zh)

<a id="english"></a>

## English

### What this skill does

`dialogue-next-steps` turns a single Q&A into a guided conversation:

1) **Deep Understanding**: infer intent, emotion, and missing key context.
2) **Precise Answer**: answer the core question clearly (with minimal necessary steps).
3) **Divergent Guidance**: when appropriate, append **up to 5 numbered next steps** so the user can continue by replying with a number.

### When it appends “Next steps”

This skill uses a gate (`add_next_steps`). It appends next steps when the user:

- Is **a beginner** or asks **conceptual/introductory** questions (even if the question is very clear).
- Asks an **underspecified** question that is not actionable without more context.
- Shows **uncertainty/emotion** where structured options reduce cognitive load.
- Explicitly asks for **suggestions / a plan / what to do next**.

It does **not** append next steps when:

- The user explicitly requests **“just the answer / no suggestions / don’t ask follow-ups”**.
- The request is **advanced and execution-ready** (well-scoped; enough context provided), and there are no beginner signals.

### Suggestion threshold (avoid fatigue)

- **0 items**: trivial one-off prompts.
- **1–2 items**: simple prompts with one obvious continuation.
- **3 items (default)**: beginner learning, missing context, or multiple plausible directions.
- **4–5 items**: only when there are truly multiple meaningful branches and each is distinct.

### Five angles for generating next steps

Candidates come from multiple angles (do not force all five every time):

- **[Depth]** deepen one key concept/step
- **[Breadth]** expand to adjacent topics / comparisons
- **[Practice]** convert into an actionable exercise / template / checklist
- **[Critical]** consider limits, risks, counterexamples, failure modes
- **[Resources]** neutral, reputable resources/tools (prefer official + free/open)

### De-duplication and prioritization

- Draft more candidates (e.g., 6–10), keep the best **<= 5**.
- Remove near-duplicates; each item must advance a **different** decision/action.
- If missing context blocks action: put **1 key clarifying item first** (max 1–2 clarifying items).
- Typical default priority: **Depth > Breadth > Resources**, but promote:
  - **Practice** when the user wants to build/try immediately.
  - **Critical** for high-stakes or controversial topics.

### Continuity (number replies)

If the user replies with a number (e.g., “2”, “pick 2”, “2 and 3”):

- Treat it as a chosen direction.
- Continue based on **(original question + chosen item)**.
- Generate the next “Next steps” based on the new context (do not restart).

### Output format

- **Always answer first**.
- If gated on, append a localized heading and a numbered list.

Example skeleton:

- Next steps (reply with a number, up to 5)
  1. [Depth] ...
  2. [Practice] ...
  3. [Breadth] ...
  4. [Critical] ...
  5. [Resources] ...

---

<a id="zh"></a>

## 中文

### 这个 Skill 做什么

`dialogue-next-steps` 把“一问一答”升级成“可续聊的引导式对话”，内部流程固定三步：

1) **深度理解**：不仅理解语义，还要推断**意图、情绪**与**缺失的关键信息**。
2) **精准回答**：先把核心问题回答清楚（只给必要步骤）。
3) **发散引导**：在需要时追加**最多 5 条带编号的下一步建议**，用户可以直接回“1/2/3…”继续。

### 什么时候会输出“下一步”

Skill 内部用一个开关（`add_next_steps`）决定是否追加下一步：

会追加（`add_next_steps = true`）：

- **入门/概念学习型**问题（即使问题很明确也要追加）。
- 问题**过泛/缺上下文**，不补信息就无法给出可执行结论。
- 用户表现出**不确定/焦虑/犹豫**，需要结构化选项降低认知负担。
- 用户明确要：**建议/计划/下一步/怎么继续**。

不会追加（`add_next_steps = false`）：

- 用户明确说：**“只要答案/不要建议/别追问”**。
- 问题**进阶且可闭环执行**（信息足够，回答后能立刻行动或验证），且用户没有学习型信号。

### 建议条数阈值（避免建议疲劳）

- **0 条**：极简/一次性问题。
- **1–2 条**：简单问题，只有 1 个明显的后续方向。
- **3 条（默认）**：入门学习、缺上下文、或有多条合理路径。
- **4–5 条**：只有在确实存在多条分支且每条都明显不同、有价值时才给。

### 生成建议的 5 个角度

建议来自不同角度（不要求每次凑满 5 个角度）：

- **[深挖]** 纵向深入一个关键点
- **[拓展]** 横向连接相邻主题/对比项
- **[实操]** 给出下一步可执行动作/练习/模板
- **[批判]** 反例、边界、风险、失败模式
- **[资源]** 中立、权威、可用的资源/工具（优先官方与免费/开源）

### 去重与排序

- 先多生成候选（如 6–10 条），再筛到最终 **<= 5**。
- 每条建议必须推进**不同的决策或动作**，语义近似的要合并。
- 若缺关键上下文：第 1 条放**最关键的澄清**（总澄清不超过 1–2 条）。
- 通常优先级：**深挖 > 拓展 > 资源**；但当用户想马上动手时上调 **实操**，高风险/争议话题上调 **批判**。

### 上下文延续（用户回编号）

当用户回复编号（如“2”“选2”“2和3”）：

- 视为用户选中的方向。
- 用“原问题 + 选中项”作为新目标继续。
- 新一轮的建议必须基于新的上下文，不要从头再来。

### 输出格式

- 永远先给**精准回答**。
- 若触发追加，则输出本地化标题 + 编号列表（最多 5 条）。

示例骨架：

- 下一步（回复编号即可，最多 5 条）
  1. [深挖] ...
  2. [实操] ...
  3. [拓展] ...
  4. [批判] ...
  5. [资源] ...

### 边界处理

- 极其简单的问题（如“你好”“几点钟了”）：可以不输出，或只给 1–2 条通用选项。
- 用户明确表示“不需要建议/就这样吧”：不再追加下一步，也不反复追问。
- 避免把用户引导到付费或特定商业产品；如需工具推荐，保持中立并优先免费/开源/官方资源。