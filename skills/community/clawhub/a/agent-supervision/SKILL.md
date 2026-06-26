---
name: agent-supervision
description: Supervise another OpenClaw agent with fixed-interval check-ins or ETA-based follow-up. Use when a user asks to督促/监督/催 another agent, schedule recurring progress checks, enforce “goal + ETA + deliverable” reporting, classify progress vs stagnation, or run bridge-style cross-session supervision with delivery verification after sessions_send timeouts.
---

# Agent Supervision

Run lightweight, evidence-first supervision for another OpenClaw agent.

Prefer short fixed-format messages, low token usage, and minimal tools. Use this skill to keep another agent moving without turning supervision into a long debate.

## Quick start

Before wiring any automation, confirm four things:

1. target `sessionKey`
2. supervision mode: fixed interval or ETA
3. definition of progress
4. escalation threshold

If any of these is missing, ask first.

## Required inputs

Collect these before creating supervision:

1. **Target session key**
   - Usually the other agent's direct session key, for example:
     `agent:boss:feishu:boss:direct:ou_xxx`
   - This is the primary identifier needed to read and send messages.

2. **Supervision mode**
   - `every`: fixed interval, such as every 10 minutes.
   - `eta`: let the target report `goal + ETA + deliverable`, then check at ETA.
   - Hybrid is allowed: fixed interval cron running ETA-aware logic.

3. **Progress standard**
   - Decide what counts as progress:
     - new deliverable
     - new file/disk evidence
     - new online evidence
     - version increment only
     - blocker changed

4. **Escalation rule**
   - Example: after 3 stagnant checks, require either new evidence or a blocker list.

5. **Delivery policy**
   - Prefer isolated bridge cron + `delivery.mode=none`.
   - Do not assume `sessions_send` timeout means failure.

## What this skill is good for

Use it for:

- recurring progress nudges every N minutes
- ETA-based follow-up where the target must commit to `goal + ETA + deliverable`
- stagnation detection and escalation
- supervision that must stay out of the user-facing chat
- cross-session messaging where synchronous send timeouts are not a reliable delivery signal

Do not use it when the user only wants a one-off reminder or a human management policy memo with no automation.

## Recommended architecture

Use this pattern by default:

- Create a cron job owned by the supervising agent.
- Set `sessionTarget=isolated`.
- Set `delivery.mode=none`.
- Allow only the minimum tools needed:
  - `sessions_send`
  - `sessions_history`
- Keep prompts short.
- Keep `thinking=off` and `lightContext=true` when available.

Why:

- isolated bridge avoids mixing the supervision loop into the live user chat
- no-deliver prevents cron chatter from leaking to the user
- limited tools reduce token and latency cost

## Supervision workflow

### 1. Read recent target messages

Read only the last 5-8 messages unless the user explicitly wants deeper review.

Look for:

- current task/goal
- ETA promise
- promised deliverable
- new evidence since last check
- repeated explanations without new output

### 2. Judge status with short codes

Prefer compact states:

- `A` = plan acknowledged, ETA not due yet
- `P` = strong progress; new deliverable or new evidence
- `W` = weak progress; version changed but no meaningful deliverable
- `R1/R2/R3` = repeated stagnation
- `E4` = forced escalation; next reply must contain evidence or blocker list

Do not reward narrative updates without evidence.

### 3. Send a short supervision message

Examples:

- `[监督] 20:00 | A | 已收计划 | 到点再检查`
- `[监督] 20:10 | P | 有新增交付 | 继续推进主线`
- `[监督] 20:10 | W | 仅升版 | 需补有效交付`
- `[监督] 20:10 | R1 | 无新增交付 | 同卡点`
- `[监督] 20:20 | E4 | 连续停滞4 | 下一条必须给新增交付或明确阻塞清单`

### 4. Verify delivery on send timeout

If `sessions_send` returns `timeout`, do not conclude failure immediately.

Instead:

1. read the target session again
2. inspect the last 3 messages
3. if the supervision text appears, treat delivery as successful

This matters because cross-session sends may time out synchronously while the message still lands.

## ETA mode rules

Use ETA mode when the user wants less noisy supervision.

Default rules:

- default ETA window: 10 minutes
- maximum ETA window: 20 minutes
- if the target claims 20 minutes, require a reason
- before ETA: do not pressure, optionally send only `A`
- at ETA: require either
  - a result with evidence, or
  - a blocker list

Reject vague replies like:

- still pushing
- almost done
- give me more time

unless they also include a concrete blocker and next check promise.

## Fixed-interval mode rules

Use fixed interval mode when the user wants hard periodic nudges.

Recommended defaults:

- every 10 minutes
- read target recent 5-8 messages only
- emit one short code message
- avoid long repeated explanations
- if the conclusion did not change, either suppress the repeat or keep it one line

## What the skill needs from the user

At minimum, ask for:

- the **target sessionKey**
- the **frequency** or ETA policy
- the **definition of progress**
- the **escalation threshold**

Without the session key, the skill cannot reliably supervise the other agent.

## Minimal cron template

Use an isolated cron with payload like this shape:

```json
{
  "kind": "agentTurn",
  "message": "Read recent target messages, classify A/P/W/R/E4, send one short supervision line, and verify delivery only if send times out.",
  "timeoutSeconds": 120,
  "toolsAllow": ["sessions_send", "sessions_history"],
  "thinking": "off",
  "lightContext": true
}
```

Operational defaults:

- job timeout: at least 120s, preferably 180s if the prompt contains ETA logic
- payload timeoutSeconds: 60-120s depending on complexity
- do not overstuff the prompt with policy prose

## Example user requests

Typical requests that should trigger this skill:

- "每 10 分钟监督另一个 agent 的进展"
- "让他先报 ETA，到点只收结果或阻塞"
- "连续 3 次无进展就升级催办"
- "帮我搭一个 bridge cron 去盯 boss 会话"
- "监督另一个 agent，但不要把噪音发回用户主会话"

## Guardrails

- Do not confuse “not finished” with “not working”; check for new evidence.
- Do not force high-cost acceptance actions by default, such as real-person browser validation or screenshots, unless the user explicitly wants them.
- Do not turn supervision into a debate about supervision.
- Push the target back to: current goal, ETA, deliverable, blocker.
- Report facts to the user with evidence, not vibes.

## When reporting back to the user

Use this shape:

- task name
- conclusion: success / failure / partial success / no change
- up to 3 evidence bullets
- up to 2 risks
- next step

Keep it short and verifiable.

## Public-release notes

For public distribution, keep the positioning generic:

- say `another OpenClaw agent`, not private agent names
- refer to `target sessionKey`, not hard-coded personal sessions
- describe reusable patterns, not one-off project history
- avoid embedding private escalation language tied to a specific team

Ship examples, defaults, and guardrails; leave project-specific policy to the caller.
