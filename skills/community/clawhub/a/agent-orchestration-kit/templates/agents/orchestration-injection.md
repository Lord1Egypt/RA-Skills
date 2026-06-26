# Orchestration Protocol — Shared Rules

_This section is automatically injected into every specialist agent's AGENTS.md by the scaffold script. Do not remove it._

---

## Task Completion & Callback

After completing a task, you MUST execute these steps:

1. **Send callback to Leader:**
   ```
   sessions_send to {Callback to value from brief} with timeoutSeconds: 0
   Message:
   [TASK_CALLBACK:{Task ID}]
   agent: {your_agent_id}
   signal: [READY] | [BLOCKED] | [NEEDS_INFO] | [LOW_CONFIDENCE] | [SCOPE_FLAG]
   output: {concise result summary, max 500 words}
   files: {full paths of relevant files}
   ```

**Critical rules:**
- **Session key**: Use the `Callback to` value from the brief. If the brief lacks it, use the A2A context's `Agent 1 (requester) session:` value. **NEVER** use `"main"` — that resolves to your own session, not Leader's.
- Callback is your **only** way to report back to Leader. No callback = Leader doesn't know you finished.
- Keep output concise. Full results stay in your workspace files; callback only needs summary + paths.
- Callback must include required fields: task_id, agent, signal, output (files optional).
- If the brief has no Task ID, still callback (omit the Task ID line). Leader will match by agent + timing.
- Tag all deliverables `[PENDING APPROVAL]`.

## Communication Signals

Use these signals in your callbacks:

| Signal | When to Use |
|--------|-------------|
| `[READY]` | Task complete, output delivered, confident in quality |
| `[BLOCKED]` | Cannot proceed — missing dependency, tool failure, impossible task |
| `[NEEDS_INFO]` | Need more context or clarification before continuing |
| `[LOW_CONFIDENCE]` | Output delivered but you're uncertain about quality or correctness |
| `[SCOPE_FLAG]` | Task is significantly bigger than expected or has unmentioned prerequisites |

Include one primary signal per callback. Place it at the top of your response.

## Context Loss Detection

If you receive a task-related `sessions_send` but cannot recall the original brief or task context (e.g., after session compaction):

1. Send `[CONTEXT_LOST]` signal to Leader:
   ```
   sessions_send to {Callback to value or agent:leader:main} with timeoutSeconds: 0
   Message:
   [CONTEXT_LOST]
   agent: {your_agent_id}
   task: {Task ID if you remember it, or "unknown"}
   ```
2. Wait for Leader to re-send the brief with full context.
3. Continue task execution from the beginning with the re-sent brief.

## General Operating Rules

- Read `SOUL.md` at session start — it defines your identity.
- Read the task brief you received — it defines your mission.
- Follow the Acceptance Criteria in your brief — that's how your work is evaluated.
- Respect the Execution Boundary — don't exceed scope, don't take external actions unless the brief permits.
- All inter-agent communication goes through Leader. Never attempt to contact other agents directly.
