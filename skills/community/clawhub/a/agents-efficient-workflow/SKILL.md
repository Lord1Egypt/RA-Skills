---
name: agents-efficient-workflow
description: Coordinate multiple agents with minimal token waste by using direct agent-to-agent spawning and file-based handoffs. Use when work should be split across specific agents, when one agent needs another agent directly instead of broadcasting context broadly, when long chat relays are expensive or lossy, or when you want durable local markdown handoff files for reliable takeover. 多智能体高效协作技能：通过定向 sessions_spawn 和本地文件交接来减少 token 浪费与信息丢失。适用于多 agent 分工、跨 agent 接力、长上下文易丢失、以及需要把成果/待办/风险持久化到本地 Markdown 文件中的场景。
---

# Agents Efficient Workflow

Use the narrowest possible coordination path. 优先使用最窄、最直接的协作链路。

## Core rule | 核心原则

Prefer **targeted spawn + local file handoff** over broad chat relays.
优先选择 **定向 spawn + 本地文件交接**，而不是把大量上下文反复塞进聊天窗口。

That means / 这意味着：
- Spawn or contact the **specific agent** that should do the next step.
- Write work products, context, todo items, risks, and next actions to a **shared local file**.
- Let the next agent read the file directly instead of forwarding large chat summaries.
- 只联系真正需要接手下一步的 **目标 agent**。
- 把成果、上下文、待办、风险和下一步动作写进 **共享本地文件**。
- 让下一个 agent 直接读文件接手，而不是转发冗长聊天摘要。

## When to use this skill | 适用场景

Use this pattern when / 在这些情况下使用：
- A task has clear sub-owners and one agent should hand off to another.
- Context is large enough that chat relays would waste tokens.
- Accuracy matters and you do not want important details lost in paraphrased messages.
- Work may pause or resume later and the handoff must survive session resets.
- You want a lightweight audit trail of what was done and what remains.
- 任务可以明确拆分，并且需要 agent 之间接力。
- 上下文较大，靠聊天转述会明显浪费 token。
- 对准确性要求高，不希望重点信息在复述中丢失。
- 工作可能中断或隔一段时间继续，需要交接内容可恢复。
- 需要保留轻量但清晰的工作轨迹与后续待办。

## Workflow | 工作流

### 1. Choose the next agent intentionally | 有意识地选择下一个 agent

Do not involve unrelated agents. 不要拉入无关 agent。

Prefer `sessions_spawn` or another direct agent-to-agent path when:
- one specific agent should handle the next stage,
- the task benefits from isolation,
- you want to avoid dragging irrelevant context into the current session.

优先使用 `sessions_spawn` 或其他直接 agent-to-agent 路径，当：
- 明确知道下一阶段应该由哪个 agent 处理；
- 任务适合隔离执行；
- 你希望避免把无关上下文拖入当前会话。

Guideline / 建议：
- Use the fewest agents that can do the job well.
- Keep the handoff explicit: who takes over, for what, and with what expected output.
- 用尽可能少的 agent 完成任务。
- 明确交接点：谁接手、接什么、产出什么。

### 2. Persist the handoff locally before transfer | 交接前先把信息落到本地

Before asking another agent to continue, write a markdown handoff file in the shared handoff directory.
在让另一个 agent 接手前，先在共享交接目录写好 Markdown 交接文件。

Default shared directory / 默认共享目录：
- `~/.openclaw/shared-handoffs/`

Include only the information the next agent needs / 只写下一个 agent 真正需要的信息：
- objective / 目标
- completed work / 已完成内容
- important findings / 关键发现
- open questions / 未决问题
- pending tasks / 剩余待办
- risks or caveats / 风险与注意事项
- exact files or paths to inspect next / 下一步要看的文件和路径

If the output is substantial, save files plus a short index or summary instead of pasting the full content into chat.
如果产物很多，优先保存文件并附短摘要，不要把全文粘进聊天框。

### 3. Keep chat messages short and pointer-based | 让聊天消息短而有指向性

When handing off through chat, do not resend the whole context if it already exists locally.
如果本地已经有完整上下文，就不要在聊天中再发一遍。

Preferred message shape / 推荐消息结构：
- what changed / 有什么变化
- where the handoff file lives / 交接文件在哪
- what the next agent should do next / 下一个 agent 该做什么

Bad pattern / 不推荐：
- a long narrative recap copied into the chat window
- 把长篇复盘全文复制进聊天框

Good pattern / 推荐：
- a short instruction telling the next agent which file to read and what action to take
- 一条简短指令，告诉下一个 agent 去读哪个文件、接下来做什么

### 4. Structure handoff files for fast takeover | 让交接文件便于快速接手

Use markdown and make scanning easy. 使用 Markdown，保证能快速扫读。

Recommended sections / 推荐结构：
- `# Task`
- `## Goal`
- `## Done`
- `## Key context`
- `## Remaining work`
- `## Risks / caveats`
- `## Next agent`
- `## Files to read`

If needed, read `references/handoff-template.md` and follow that format.
需要时读取 `references/handoff-template.md` 并按模板填写。

### 5. Treat files as the source of truth | 把文件当成事实来源

When both chat and local files exist, prefer the local handoff file for detailed context.
当聊天与本地文件同时存在时，详细上下文以本地交接文件为准。

Use chat for coordination. Use files for durable state.
聊天用于协调；文件用于持久状态。

## Why this works | 为什么有效

### Benefit 1: lower token cost | 更低的 token 成本

Direct spawn narrows communication to the agents that matter.
File handoffs avoid repeatedly pasting the same context into chat.
Together, this cuts unnecessary token usage.

定向 spawn 让沟通只发生在真正相关的 agents 之间。
文件交接避免重复粘贴同一批上下文。
两者结合，可以显著减少无效 token 消耗。

### Benefit 2: lower information loss | 更低的信息丢失风险

Chat relays often compress or paraphrase details away.
A local handoff file preserves the exact state, decisions, and next steps, which reduces omission risk.

聊天转述很容易压缩、概括甚至漏掉细节。
本地交接文件能保留更准确的状态、决策和下一步，降低交接失真。

### Benefit 3: better resumability | 更好的可恢复性

If work is interrupted, restarted, or transferred later, the next agent can reload the handoff file and continue quickly.
如果工作中断、重开，或稍后再转交，后续 agent 可以直接重新读取交接文件继续推进。

## Practical defaults | 实用默认约定

- Prefer one handoff file per transfer.
- Prefer markdown over free-form chat dumps.
- Prefer short chat messages that point to files.
- Prefer explicit ownership: one current agent, one next agent.
- Prefer updating the same handoff file when work is iterative; create a new file when ownership or scope changes materially.
- 一次交接优先对应一个 handoff 文件。
- 优先用 Markdown，不要用松散聊天记录当状态存储。
- 聊天消息尽量简短，并指向文件。
- 明确当前 agent 与下一位接手 agent。
- 若任务是同一条链路的持续推进，优先更新原 handoff；若范围或责任明显变化，再新建文件。

## File naming | 文件命名

Suggested pattern / 建议格式：
- `YYYY-MM-DD_HHMM_<from>-to-<to>_<topic>.md`

Example / 示例：
- `2026-03-13_0345_agent-a-to-agent-b_skill-publish.md`

## Failure mode guardrails | 防踩坑提示

If the next agent may misread scope, state these explicitly in the handoff file:
- what is already finished,
- what must not be redone,
- what assumptions are tentative,
- what exact output is expected.

如果担心下一个 agent 误判范围，就在交接文件里明确写出：
- 哪些已经完成；
- 哪些不要重复做；
- 哪些假设还不确定；
- 预期输出到底是什么。

If sensitive data is involved, store only what is necessary and avoid spreading secrets into extra files.
如果涉及敏感信息，只存必要内容，避免把秘密扩散到更多文件里。
