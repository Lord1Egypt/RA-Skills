---
name: executive-os
description: Build or operate a chief-of-staff style communications layer that merges multiple inboxes and chat sources into one prioritized digest with follow-up memory, decision tracking, recommendations, alerts, and a strict no-send boundary.
---

# Executive OS

Use this skill when the task is to turn mixed communications into a single operating queue rather than a source-by-source summary.

## Core workflow

1. Read `references/operating-model.md` first.
2. Read `references/registries.md` before assigning importance.
3. If persistent state is needed, read `references/persistent-memory.md`.
4. If the task includes recommendations or interruption policy, read `references/recommendations-and-alerts.md`.
5. If raw source behavior matters, read `references/source-heuristics.md`.
6. If local notes or meeting docs should shape triage, read `references/local-context.md`.
7. Read `references/safety.md` before proposing any external step.

## Output standard

Prefer this structure:

- Urgent now
- Needs reply
- Decisions pending
- Follow-ups slipping
- Important but not urgent
- FYI / low signal
- Source gaps

Keep each item short:
- one-line summary
- why it matters
- recommended next step when useful

## Operating rules

- Merge signals into one queue.
- Prefer explicit registries over generic heuristics when both exist.
- Keep follow-up and decision ledgers short and current.
- Treat unread state as weak evidence; prioritize urgency, deadlines, blocked threads, money, legal, safety, and relationship context.

## Safety

- Do not send emails, chats, or DMs to third parties without explicit approval.
- Do not click send on the user's behalf.
- Do not mutate external systems unless explicitly authorized.
- Drafting, triage, prioritization, alerting, and ledger maintenance are allowed.

If the next step becomes a risky external action, route it through an action-gate workflow instead of improvising.
