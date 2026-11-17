# Collaborate vs Delegate vs Solo — Routing the Task

The five routing checks live in SKILL.md (Collaborate vs Delegate vs Solo); run them in order, first hit wins. This file covers what each mode actually asks for, the symptoms of misrouting, and the hybrid sequences.

## What Each Mode Is

| Aspect | Delegate | Collaborate | Solo |
|---|---|---|---|
| You need | Something DONE | Something CHALLENGED or shaped | Nothing from anyone |
| Relationship | Hierarchical: you specify, they execute | Horizontal: positions meet | — |
| Brief | Complete spec + acceptance criteria | Goal + constraints + one falsifiable question (`briefing.md`) | — |
| Context given | Everything needed to execute without you | Dosed — enough to judge, not enough to inherit your frame | — |
| Expected return | A deliverable that passes the criteria | A verified claim that moves your position | The outcome itself |
| Success looks like | You did not have to think about it again | You changed something you would have shipped | Shipped, observed, moved on |
| Failure smell | Bounced deliverables, line-by-line rework | Zero movement, politeness, agreement | Expensive surprise you had a cheap way to catch |

The core distinction: delegation transfers EXECUTION and keeps judgment; collaboration borrows JUDGMENT and keeps execution. Handing off judgment ("you decide, I'll do whatever") is neither — it is abdication, and it returns whatever the counterpart's incentives return.

## Misrouting Symptoms

| Symptom | Diagnosis | Reroute |
|---|---|---|
| Delegated task bounced back wrong twice | Acceptance criteria were not actually writable | Collaborate on the spec first, then re-delegate |
| You are rewriting the delegate's output line by line | Criteria unclear, or the work needed your judgment throughout | Reclaim it solo, or pair (`pairing.md`) |
| Collaboration produced a task list, no position moved | It was delegation wearing a discussion costume | Write the criteria, hand it off |
| Exchange ended in round 1 with "sounds good" | It was solo; the counterpart could not be surprised (SKILL.md Rule 1) | Skip the exchange next time; note what made it predictable |
| You keep "collaborating" with someone who only executes your conclusions | Hierarchy mislabeled as exchange | Call it delegation; give them real criteria and autonomy |
| Delegate keeps asking judgment questions mid-task | The spec embedded decisions you had not made | Pull those decisions back, resolve (collaborate if stuck), re-issue |
| You wanted many options, got one critique | Exchange too early — nothing worth attacking yet | Diverge first; return with the strongest candidate |

## Hybrid Sequences

- **Shape → execute** (most common): collaborate to settle the approach — the exchange's decision record becomes the delegation's spec. The record's acceptance criteria ARE writable now precisely because the exchange defined them; that is the routing flip (SKILL.md Rule 2) happening live.
- **Execute → judge reception**: delegated work came back green on criteria but feels off → the criteria missed a dimension; run an audience pass (`audience-pass.md`) to name it, then amend the criteria — do not bounce the deliverable with "something's off."
- **Collaborate at boundaries only**: long solo or delegated work with exchange checkpoints at irreversible moments (design locked, API frozen, before the migration). Cheaper than pairing, catches the one-way doors; the checkpoint list is written when work starts, not improvised when confidence dips.
- **Diverge → collaborate**: generate options wide (route to `diverge`), pick the strongest, then run ONE exchange on it. Running exchanges on every divergent option burns the budget on candidates that lose anyway.

## Budget Interaction

The exchange budget (SKILL.md Rule 3: `budget_share`, default 10%, floor 5 min, cap 30 min) prices the routing decision itself: a 30 min task cannot pay for collaboration (floor barely fits — solo), a 4h task can afford 24 min of challenge, and a week-long commitment caps out at 30 min per exchange but justifies several exchanges at different boundaries. Delegation has no such cap — its budget is spec-writing time, which is why writable criteria route there first.
