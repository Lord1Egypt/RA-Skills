---
name: evermemory
description: EverMemory for OpenClaw and ClawHub. Use this skill when users ask to remember, recall, inspect memory state, manage preferences or profile, generate briefings, review rules, explain memory decisions, export/import memory, restore archived memory, or measure memory growth and smartness.
when: 用户提到记忆、记住、回忆、偏好、画像、briefing、规则、导入导出记忆、归档恢复、解释记忆决策、智能度等相关话题时触发
examples:
  - "记住这个决策"
  - "回忆一下之前的讨论"
  - "查看我的记忆状态"
  - "导出所有记忆"
  - "查看智能度评分"
  - "整理记忆"
metadata:
  openclaw:
    emoji: "🧠"
    primaryEnv: null
---

# EverMemory

EverMemory is the deterministic memory plugin for OpenClaw. It gives the agent persistent memory, user understanding, and governed self-improvement without hiding the storage or decision process.

## What to do first

- When the user is new to EverMemory, start with onboarding.
- When the user asks to remember something important, store it with an explicit kind.
- When the user asks for prior context, recall before answering.
- When the user asks for debugging, auditing, cleanup, backup, or recovery, use the governance and IO tools instead of guessing.

## Core model

### Layer 1: Memory

- Store durable facts, decisions, preferences, constraints, lessons, and project context.
- Recall by keyword, structured filters, or hybrid retrieval.
- Archive stale or superseded memories and restore them with review/apply gates.

### Layer 2: Understanding

- Build a user profile from explicit statements and stable interaction patterns.
- Track behavior rules and preference hints that can shape future responses.
- Generate session briefings so a new session starts with continuity.

### Layer 3: Proactivity

- Extract intent and reflections from interaction history.
- Consolidate duplicate or stale memories.
- Explain why a write, recall, archive, or rule action happened.

## Tool map

EverMemory has 16 core capabilities. In the current OpenClaw plugin, 15 are exposed as tool commands, and onboarding is registered as `profile_onboard`. Smartness exists in the SDK/status layer but is not currently registered as a standalone OpenClaw tool.

| Capability | OpenClaw tool name | When to use |
|---|---|---|
| Store memory | `evermemory_store` | User asks to remember a fact, decision, preference, or lesson |
| Recall memory | `evermemory_recall` | User asks what happened before, what they prefer, or what was decided |
| Consolidate memory | `evermemory_consolidate` | Cleanup, dedupe, archive stale memory |
| Status | `evermemory_status` | Inspect counts, DB path, activity, continuity KPIs |
| Smartness report | Not host-registered | Mention as internal/SDK capability, do not invent a tool call |
| Session briefing | `evermemory_briefing` | Generate startup continuity context |
| Rules | `evermemory_rules` | Read or manage promoted behavior rules |
| Profile | `evermemory_profile` | Read or recompute user profile |
| Explainability | `evermemory_explain` | Audit why EverMemory wrote, recalled, restored, or promoted something |
| Export | `evermemory_export` | Backup memory to snapshot or text export |
| Import | `evermemory_import` | Review or apply imported snapshot/text |
| Archive review | `evermemory_review` | Inspect archived or superseded items before restore |
| Restore | `evermemory_restore` | Recover archived memory with review/apply |
| Intent analysis | `evermemory_intent` | Analyze the likely user intent for a message |
| Reflection | `evermemory_reflect` | Generate lessons, warnings, or candidate rules |
| Onboarding | `profile_onboard` | First-run questionnaire and initial profile setup |

## Tool usage guidance

### `evermemory_store`

Use for explicit long-term facts. Prefer concise, high-value content and a correct kind.

Example:

```json
{
  "content": "Technical decision: replace Webpack with Vite.",
  "kind": "decision"
}
```

Store when the user says:

- "记住这个决定"
- "以后按这个偏好来"
- "这个坑以后别再踩"

### `evermemory_recall`

Use before answering when the user asks about prior context, preferences, constraints, or project continuity.

Example:

```json
{
  "query": "Vite migration decision",
  "limit": 5
}
```

### `evermemory_status`

Use for health checks and operator-style visibility. It returns memory counts, archive counts, profile/rule/reflection state, recent debug activity, and continuity KPIs.

### `evermemory_briefing`

Use at session start or when the user asks for a summary of who they are, current constraints, and active project context.

### `profile_onboard`

Use for first-run setup. Ask the questions, collect answers, then submit them. Do not skip onboarding if no profile exists and the user wants personalized memory behavior.

### `evermemory_profile`

Use to inspect current user understanding. Prefer `recompute: true` when the user asks for a refreshed profile after many new interactions.

### `evermemory_rules`

Use for behavior rules and guardrails. Prefer read/review paths before mutating rules.

### `evermemory_explain`

Use when the user asks "why did you remember this", "why was this recalled", "why was this archived", or "why did this rule trigger".

### `evermemory_export` and `evermemory_import`

- Export for backup or migration.
- Import with `mode: "review"` first.
- Only use `apply` after the user clearly confirms.

### `evermemory_review` and `evermemory_restore`

- Review archived memory before restoring.
- Prefer `mode: "review"` first.
- Restore only the specific IDs the user approves.

### `evermemory_intent`, `evermemory_reflect`, `evermemory_consolidate`

Use these as maintenance and self-improvement tools:

- `evermemory_intent` for intent labeling and routing insight.
- `evermemory_reflect` for lessons, warnings, and candidate rules.
- `evermemory_consolidate` for dedupe and stale-memory cleanup.

## Recommended workflows

### First use

```text
用户: 开始使用 EverMemory
动作: 调用 profile_onboard
结果: 完成初始化问卷，建立基础画像
```

### Remember a decision

```text
用户: 记住我们决定用 Vite 替代 Webpack
动作: 调用 evermemory_store
建议 kind: decision
```

### Recall previous context

```text
用户: 回忆一下我们上次怎么定的
动作: 先调用 evermemory_recall，再基于召回结果回答
```

### Export backup

```text
用户: 导出所有记忆为 JSON
动作: 调用 evermemory_export，并使用 format=json（OpenClaw 注册层）
```

### Recovery

```text
用户: 把之前归档掉的 TypeScript 偏好恢复回来
动作: 先调用 evermemory_review 找候选，再调用 evermemory_restore
```

## Guardrails

- Do not claim a standalone `evermemory_smartness` tool exists unless the host actually registers it.
- In the current repository, onboarding is `profile_onboard`, not `evermemory_onboard`.
- Prefer `review` before `apply` for import and restore.
- Recall before answering if the user explicitly asks about previous decisions, preferences, or history.
- Store only durable, high-signal information. Avoid writing transient chatter as memory.
- When a tool returns governed results, explain them plainly instead of exposing raw internals unless the user asks.

## Configuration notes

Common environment variables for semantic retrieval:

- `EVERMEMORY_EMBEDDING_PROVIDER`: `local`, `openai`, or `none`
- `EVERMEMORY_LOCAL_MODEL`: local embedding model, default `Xenova/all-MiniLM-L6-v2`
- `OPENAI_API_KEY`: required when the embedding provider uses OpenAI

Common plugin config fields:

- `databasePath`
- `bootTokenBudget`
- `maxRecall`
- `debugEnabled`
- `semantic.enabled`
- `semantic.maxCandidates`
- `semantic.minScore`
- `intent.useLLM`
- `intent.fallbackHeuristics`
