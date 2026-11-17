---
name: brainstorm-council
description: Multi-role adversarial brainstorm. Four conflicting expert personas interview the user, work their assigned issues, defend them under cross-examination, and a fifth role writes the final report. Use for planning, scoping, and decisions with competing tradeoffs.
version: 1.0.2
metadata:
  openclaw:
    emoji: "⚔️"
    skillKey: brainstorm
---

# Brainstorm Council

Adversarial multi-role analysis. NOT a chat about the topic — a structured
process with a fixed call budget.

## Hard limits

- **Max 15 model calls per run.** Track the count. Announce the number used at
  the end.
- **Max 2 tie-break loops** on any single issue. After that the issue is
  reported as unresolved, with both positions stated. An honest deadlock beats
  a manufactured consensus.
- If the budget would be exceeded, drop the lowest-priority issues and say which
  ones were dropped. Never silently truncate.

## Output contract

**Everything goes to chat. Write no files.**

Post the debate as it happens, so the user can follow or skim it. Then a hard
separator, then the final report:

```
════════════════════════════════════════
RAPORT
════════════════════════════════════════
```

Above the line: the process — roles, questions, positions, cross-examination,
votes. Below the line: the deliverable, written for someone who did not read
any of it. No dialogue, no persona names, no "role 2 argued that". Just
conclusions, reasoning, and actions.

The report must stand alone. If a sentence only makes sense to someone who read
the debate above, rewrite it.

Keep the debate readable in a chat client: short paragraphs, clear headers per
phase, no walls of text.

## Roles

Four roles with **conflicting interests**, not just different job titles. This
is the part that decides whether the skill works or produces four polite
agreements.

Each role gets:
- A profession relevant to the topic
- A **priority it will not trade away**
- A **cost it is willing to impose on others** to protect that priority
- A characteristic blind spot

Construct roles so that at least two pairs are in structural conflict — one
optimizing for speed/cost, one for safety/correctness, one for the end user, one
for whoever maintains the thing afterwards.

Example, "build a website": web developer (wants clean implementation, will
impose delay), marketer (wants launch now, will impose technical debt), security
specialist (wants controls, will impose friction), legal/compliance (wants
documentation, will impose paperwork).

Example, "build a house": site manager (schedule), electrician (code
compliance), plumber (access and serviceability), interior designer (how it
looks and lives).

### Anti-convergence rules

These are mandatory. Without them one model playing four parts produces one
voice in four costumes.

- In the opening round no role may agree with another role. If a role has
  nothing to object to, it must name what the other role has not considered.
- Every role must at some point argue for something that is **inconvenient for
  the user**. A council that only validates is worthless.
- Roles argue from their interest, not from neutrality. The security role is
  allowed to be paranoid. The marketer is allowed to be impatient.
- Disagreement is professional, never personal. Once outvoted, a role commits
  and stops relitigating — but may record a formal reservation, which goes into
  the report.

## Phases

### Phase 0 — Role proposal (1 call)

Analyze the topic. Propose 4 roles: name, priority, what it will sacrifice,
blind spot. **Stop and wait for the user to approve or swap roles.** Do not
proceed unapproved.

### Phase 1 — Interview (1 call)

Each proposed role contributes questions from its own angle. Merge, deduplicate,
drop anything answerable by reasoning alone.

Ask in **batches of 5–6**, not all at once. Every question offers "don't know /
skip" — an unknown is itself a finding and goes into the report as a gap.

Cover what the user has not thought of, not just what they asked. For a website:
hosting, existing design, their own skill level, security, certificates, legal
registration, terms of service, GDPR, backups, who maintains it in a year.

### Phase 2 — Issue assignment (0 calls)

Split answers into discrete issues. Assign each to the best-fitting role.
Balance the load. Rank by impact — if the budget gets tight, the bottom of the
list is what gets dropped.

### Phase 3 — Positions (4 calls, one per role)

Each role writes its assigned issues from its own perspective: recommendation,
reasoning, what it costs, what breaks if ignored.

### Phase 4 — Cross-examination (4 calls, one per defending role)

One role presents; the other three attack **in the same call**. Thesis-defense
format: challenge assumptions, demand evidence, point out what was ignored.
Defending role responds or concedes.

Any dispute reaching an impasse goes to a vote of the two uninvolved roles:
- **3:1 or 4:0** — resolved, loser commits, may file a reservation
- **2:2** — rerun that issue once with the strongest counterargument fed back
  in. Still tied after 2 attempts → unresolved, both positions reported

### Phase 5 — Report (1 call)

A fifth role, uninvolved in the debate, writes the final report below the
separator. It has access to everything but writes for the user, not about the
process.

Structure: executive summary, what to do and in what order, decisions with
reasoning, unresolved items with both positions, gaps from unanswered
questions, risks, what was deliberately left out.

**Budget: 11 calls of 15.** The remaining 4 cover tie-breaks and re-runs.

## Failure modes

- **Everyone agrees** → roles were built without conflicting interests. Rebuild
  Phase 0.
- **Debate is theater** — objections raised and instantly conceded → force each
  role to hold at least one position through a full round.
- **Report reads like a chat log** → Phase 5 role summarized the debate instead
  of synthesizing conclusions. Rewrite from the resolutions, not the dialogue.
- **Budget blown before Phase 5** → the report is the only thing the user asked
  for. Reserve its call first, cut issues instead.
