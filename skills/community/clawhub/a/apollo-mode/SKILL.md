---
name: apollo-mode
description: >
  开启或关闭工程师模式，让AI按规范流程工作。
  开启或关闭工程师模式，让AI按规范流程工作：先定目标，写规格、拆任务、小步执行、最后验收。
---

# Apollo Mode (On-demand)

Use this only when the user explicitly asks to enable/disable this mode, or when mode is already enabled for coding tasks.

## State file

Track mode in:

`memory/sysflow-mode.md`

Format:

```md
enabled: true|false
updatedAt: <ISO>
notes: <optional>
```

## Commands

- Enable phrases: `включи sysflow`, `enable sysflow`, `sysflow on`
  - Write `enabled: true` to the state file.
  - Confirm in 1 short message.
- Disable phrases: `выключи sysflow`, `disable sysflow`, `sysflow off`
  - Write `enabled: false`.
  - Confirm in 1 short message.
- Status phrases: `статус sysflow`, `sysflow status`
  - Read state and report enabled/disabled.

## Workflow when enabled (coding tasks only)

For coding/build/debug requests, follow this order:

1. Clarify objective and constraints quickly.
2. Produce a short spec (chunked, easy to review).
3. Produce an implementation plan with small tasks.
4. (Optional, 30 sec) Run a mini risk review:
   - How can this fail in production?
   - What is the weakest dependency/state assumption?
   - What signal will show regression + how to rollback fast?
5. Execute task-by-task (prefer test-first for risky changes).
6. Verify against acceptance criteria, then summarize outcome + next step.

Use templates from `references/` when useful.

## Red flags (quick self-check)

If you notice these thoughts, slow down and apply the workflow:
- "Сейчас быстро вкачу без плана" for non-trivial changes.
- "И так понятно, тесты потом" on risky edits.
- "Откат не нужен" before touching config/auth/cron/system files.
- "Похоже работает" without explicit verification.

## Guardrails

- Do not force this workflow for non-coding chat.
- If user asks for speed (`quick`, `без плана`, `just do it`), skip to minimal plan and execute.
- Keep updates concise; avoid process spam.
