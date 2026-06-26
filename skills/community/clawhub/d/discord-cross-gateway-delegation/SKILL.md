---
name: discord-cross-gateway-delegation
description: "Set up and operate full cross-gateway task delegation between two OpenClaw Discord bots across different PCs/gateways. Use when: another OpenClaw bot lives on a different machine and you want private-lane delegation, structured worker protocols, DM natural-language triggers, worker-side intake, and result relay-back into the original DM. Triggers: 'delegate work to another OpenClaw bot', 'cross-gateway delegation', 'connect another gateway bot', 'Discord worker bot setup', 'maekjini', 'kaijini', 'worker lane', 'DM auto delegation'. NOT for: same-gateway session routing, normal DM chat without delegation, or non-Discord automation."
---

# Discord Cross-Gateway Delegation

Run a full Discord-based delegation loop between two OpenClaw bots on different PCs/gateways.

## Core rule

Treat the second bot as an **external worker**, not as an internal session.
Do **not** use same-gateway assumptions like `sessions_send`, local subagents, or same-process routing.

## Supported operating model

A complete delegation flow should include all of these stages:

1. private delegation lane setup
2. structured task envelope protocol
3. optional DM natural-language trigger on the controller side
4. worker-side intake in the delegation lane
5. worker started/final replies in the lane
6. relay-back of the final worker result into the original DM

If only steps 1-2 are working, the setup is incomplete.

## Protocol rule

Use a protocol namespace that matches the worker lane.

Examples:

- MACJINI lane: `[MAC_TASK]`, `[MAC_STATUS]`, `[MAC_DONE]`
- KAIJINI lane: `[KAI_TASK]`, `[KAI_STATUS]`, `[KAI_DONE]`

Do not mix worker identity and protocol prefix unless you are intentionally keeping a legacy compatibility layer.

## What to read first

1. `references/setup-checklist.md`
2. `references/operating-modes.md`
3. `references/full-process.md`
4. If the worker is a secondary execution bot, `references/macjini-rollout.md`
5. If anything fails, `references/diagnosis.md`

## Operating guidance

- Prefer a **private server delegation lane** over public channels.
- Support both **quick handoff** and **orchestrated handoff**.
- For real work, prefer **orchestrated handoff**: the controller bot should understand the task first, generate the worker-facing envelope itself, then delegate.
- Keep quick handoff as a shortcut for simple tests and short tasks.
- Test **DM trigger**, **lane intake**, and **DM relay-back** as separate checkpoints.
- Consider the setup successful only when the final worker result appears back in the original DM.
- A lane message alone is not success.
- A worker reply in the lane alone is not success.

## If channel messages fail

Read `references/diagnosis.md`.
If the worker bot responds in DM but not in server channels, first assume a guild-channel inbound policy issue.
For `groupPolicy: allowlist`, explicitly add the target guild/channel under `guilds`, then re-test channel-based worker intake before falling back.
