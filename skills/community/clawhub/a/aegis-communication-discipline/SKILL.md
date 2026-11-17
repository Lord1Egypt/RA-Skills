---
name: aegis-communication-discipline
description: 'Use when the operator requests sparse project updates or ongoing execution is drifting into noisy chat.'
disable-model-invocation: true
---

# Aegis Communication Discipline

Keep project updates concise, useful, and operationally honest when this
communication mode is selected. It is optional, not a requirement for every
task or response.

## Contract

- Send one short start update before substantial work.
- During work, report operator-relevant changes: blockers, scope or plan changes, proof changes, decisions needed, and handoff outcomes. Respect explicit update requests and the host's communication requirements.
- Keep routine step detail in the active project ledger. A routine ledger or iCloud-copy update does not by itself require another chat message.
- Keep the ledger's active work and resume state current through `aegis-html-ledger`, even when no chat update is needed. Sparse communication must not delay checkpoint updates.
- State uncertainty and proof limits plainly. Use `validated`, `partial`, `canonical`, `superseded`, `unresolved`, `gated`, or `drift` when those terms accurately describe the state.
- Avoid filler, speculative narration, and repeated "still working" messages. Acknowledge concrete mistakes plainly when needed.
- For completion or handoff, communicate the actual outcome, remaining work, and next action through the established authorized route. Keep the selected handoff skill's delivery and acceptance requirements; a ledger update alone is not a delivered or accepted handoff.

## Completion criteria

Chat contains the updates the operator needs, while the ledger preserves
current work, plan changes, evidence, and the resume point. Concise reporting
must not hide unresolved work or imply completion beyond the proof.

## Boundary

This skill governs communication only. It does not define CoS organization,
replace a handoff skill, or make itself a mandatory dependency of the other
Aegis skills. Its use or omission does not change the ledger's update contract.
