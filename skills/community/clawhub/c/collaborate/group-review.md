# Group Review — More Than Two Parties

A group is justified only when multiple parties own DIFFERENT consequences (security, ops, product each pay for a different failure). If everyone would lose the same way, that is one lens wearing several faces — run a single-counterpart exchange instead (SKILL.md Counterpart Selection).

## Setup Before Anyone Speaks

- **One named decision owner**, declared before the review starts. Reviews advise; the owner decides. No owner declared = design by committee, and the loudest lens wins by default.
- **Reviewers invited by lens coverage, not seniority.** Each reviewer maps to a distinct loss function (`counterparts.md` catalog); two reviewers with the same lens forward their comments through one of them. Extra same-lens reviewers add signatures, not information.
- **The artifact is a written document** with the position, constraints, and the falsifiable questions per lens (`briefing.md`). No document = the review will re-derive context live and spend its budget on alignment, not critique.

## Written-First Protocol

1. Reviewers comment on the document asynchronously, before any live session. Written comments are independent; live first-reactions anchor on whoever speaks first (same failure as SKILL.md Rule 5, at group scale).
2. Every reviewer labels their own comments: **blocking** (decision must not proceed until resolved) / **non-blocking** (should fix, does not gate) / **preference** (author may ignore). The author never downgrades someone else's label — they resolve or contest it.
3. The author resolves in writing what can be resolved in writing.
4. Live session, if needed at all, covers ONLY the contested blocking threads — with the exchange budget (SKILL.md Rule 3) applied per thread, not per meeting.
5. The owner decides; the record (`convergence.md`) lists each unresolved blocking objection as a surviving objection with its trigger.

## Sign-Off Rules

- Silence is not approval. Each declared lens signs off explicitly or their named concern goes in the record as unassessed risk.
- A blocking label requires a falsifiable reason ("this violates X, observable as Y"). "I'm not comfortable" is a preference wearing a blocking costume — the owner may contest it back to preference.
- Fundamental objections have a deadline: end of the written round. The drive-by reviewer who appears at decision time with "why does this exist at all" reopens nothing unless they bring evidence the written round lacked — otherwise their objection is recorded for the next revisit, not this decision.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Review as approval ritual | Reviewers sense the decision is made; they perform diligence | If the decision is made, say so and ask only for risk spotting |
| Live-first review | First speaker anchors the room; independent signal destroyed | Written comments before any meeting |
| Owner-less review | Converges on the average of all lenses — incoherent by Rule 7 | Name the owner before inviting anyone |
| Resolving preference comments | Author burns budget polishing to taste while blocking threads wait | Triage order: blocking → non-blocking → done |
| Headcount as rigor | Ten same-lens reviewers = one opinion, ten signatures | Invite by distinct loss function only |
| Endless comment threads | A thread past a few exchanges is a two-party deadlock in public | Move the two parties to a bounded exchange (`deadlock.md`), report the result back |
