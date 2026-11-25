---
name: agent-handoff-protocol
version: 1.0.0
description: Hand work between agents (or between an agent and a human) without losing state: the handoff packet format and the acceptance checks. Use whenever work passes from one worker to another.
---

# Agent Handoff Protocol

## Overview

Handoffs are where multi-agent work goes to die: context assumed, state ambiguous, completion unverifiable. This protocol makes every handoff a packet — goal, state, evidence, open questions — that the receiver verifies before starting.

## When to use

Whenever delegating to another agent, shifting work between sessions, or handing agent work to a human for continuation.

## Workflow

1. **Write the goal** — one sentence, plus the definition of done in observable terms
2. **Write the state** — what is done (with evidence links), what is in progress, what is untouched; never 'mostly done'
3. **List the artifacts** — every file, URL, and ID the receiver needs, verified to open
4. **List the traps** — what already failed, what must not be retried, and any irreversible step already taken
5. **List the open questions** — each with its default if unanswered, so the receiver is never fully blocked
6. **Receiver acceptance** — the receiver restates goal and state in their own words before starting; mismatches get resolved first, not discovered later

## Guardrails

- Never hand off an irreversible action with an unknown outcome — resolve or flag it first
- Never include secrets in a handoff packet; reference where they live instead
- A handoff without evidence links is a rumor, not a state

## Output format

A handoff packet: goal, definition of done, state with evidence, artifacts, traps, open questions with defaults.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
