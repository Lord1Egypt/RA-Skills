---
name: Collaborate
slug: collaborate
version: 1.0.3
changelog: "Display name shown correctly"
description: >-
  Structures collaboration: picks the counterpart, runs a bounded exchange on a plan or decision, lands a decision or a recorded disagreement. Use when a plan needs critique, red-teaming, or a devil's advocate before commitment, when giving or asking for a second opinion, design review, or feedback on a draft, when a review thread keeps looping without anyone changing position, when a group review or pairing session needs structure, or when choosing between collaborating, delegating, and working solo. Not for routing specified work to sub-agents — that is delegation.
homepage: https://clawic.com/skills/collaborate
metadata:
  clawdbot:
    emoji: "🤝"
    displayName: Collaborate
    configPaths:
    - ~/Clawic/data/collaborate/
---

Decision records and user preferences live in `~/Clawic/data/collaborate/` (`decision-log.md` for the record format). If you have data at an old location (`~/collaborate/` or `~/clawic/collaborate/`), move it to `~/Clawic/data/collaborate/`.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/collaborate/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| round_cap | number (1-5) | 3 | Hard stop in Running the Exchange; the two-round no-movement rule still fires first |
| budget_share | number (% of task estimate) | 10 | Scales Rule 3's exchange budget; the 5 min floor and 30 min cap stay fixed |
| solo_undo_threshold | number (minutes) | 15 | Undo cost below this (with blast radius limited to you) routes to solo in the routing checks |
| counterpart_mode | auto \| recruit \| simulate | auto | auto recruits a real human or agent when one is reachable, otherwise simulates the counter-mindset; recruit/simulate force one side |
| log_decisions | bool | true | Append every convergence record to `~/Clawic/data/collaborate/decisions.md` |

Preference areas to record as the user reveals them:

- **counterpart pool** — who is recruitable (teammates, review groups, other agents, nobody) — resolves `counterpart_mode` and shapes Counterpart Selection
- **record conventions** — where decisions live (team ADRs, repo docs, the decision log) and their format — affects Convergence and `decision-log.md`
- **escalation path** — who breaks deadlocks and what counts as blocking — affects `deadlock.md`
- **critique register** — how blunt critique to and from humans should be — affects `with-humans.md` and `group-review.md`

## When To Use

Mode: act-as. The agent runs the exchange itself, with a real second party (human, another agent) or by fully adopting a counter-mindset for the round.

- A plan feels solid but nobody has attacked its assumptions yet
- Two options both look defensible and you keep re-reading them without deciding
- An artifact is technically correct but you cannot judge how its audience will receive it
- You are about to commit to something expensive to undo and your confidence came cheap
- You and another party keep exchanging messages without anyone changing position
- A review, critique session, or pairing setup needs structure so it ends in a decision, not a thread
- Not for routing specified work to sub-agents (that is delegation) or fanning out many parallel viewpoints (that is divergence)

## Quick Reference

| Situation | Play |
|---|---|
| Confident plan, never attacked | Adversarial round: 1 counterpart attacks the 3 assumptions that, if false, kill the plan (`adversarial-review.md`) |
| Two defensible options, stuck | Loss-function swap: judge each option as the person maintaining it 6 months from now (`second-opinions.md`) |
| Correct output, unknown reception | Audience pass: one round as the least patient consumer of the artifact (`audience-pass.md`) |
| Undo cost under 15 min, blast radius only you | Solo; the exchange costs more than the mistake |
| Acceptance criteria writable right now | Delegate instead; collaboration adds latency, not information (`vs-delegate.md`) |
| Two rounds, zero position movement | Stop; record decision + surviving objection + revisit trigger; escalate only if blocking (`deadlock.md`) |
| Counterpart shares your data and your incentives | Replace them or feed them different data; otherwise skip the exchange (`counterparts.md`) |
| Review needs 3+ stakeholders | Written comments first, one named decision owner, blocking/non-blocking triage (`group-review.md`) |
| Critique must land on a human author | Goal first, one falsifiable concern per point, severity label on each (`with-humans.md`) |
| Counterpart is another agent instance | Fresh context, counter-role with a loss function, blind first pass (`with-agents.md`) |
| Too ambiguous to spec, too costly to review after | Pair live: driver/navigator with rotation at natural boundaries (`pairing.md`) |
| Anything else | One counterpart, position written first, 3-round cap, converge to one design |

Depth on demand: `adversarial-review.md` attacking plans · `second-opinions.md` choosing between options · `audience-pass.md` reception testing · `counterparts.md` catalog and simulation discipline · `briefing.md` context dosing and the falsifiable question · `deadlock.md` stuck exchanges, disagree-and-commit, escalation · `convergence.md` decision records and revisit triggers · `group-review.md` multi-party reviews · `with-humans.md` politeness and power · `with-agents.md` agent counterparts · `pairing.md` live driver/navigator work · `vs-delegate.md` routing between modes · `decision-log.md` persistent record format.

## Core Rules

1. **Collaborate only where you can be surprised.** Test: write the counterpart's predicted response in one sentence. If you can predict it AND you know what you would do with it, apply that and skip the exchange. A collaboration that cannot move you is theater.
2. **Route by acceptance criteria.** Criteria writable now → delegate. Criteria not writable yet because defining them IS the work → collaborate. Criteria writable and undo cost under `solo_undo_threshold` (default 15 min) → solo. Example: "refactor module X, tests stay green" is delegable; "should this module exist" is collaborative.
3. **Budget the exchange at `budget_share` (default 10%) of the task estimate, floor 5 min, cap 30 min.** 4h task → 24 min of exchange. 30 min task → budget hits the 5 min floor, which usually means solo. Past the cap you are negotiating, not learning.
4. **Counterpart must differ in loss function or information, ideally both.** Same incentives + same inputs = echo with extra steps. Prefer the counterpart who loses something if you are wrong over the one who wants you to feel good.
5. **Write your position before exposure.** One paragraph: decision, strongest reason, kill condition (what would change your mind). No kill condition = you want validation, not collaboration. Unanchored exchanges converge on whoever speaks first, not on whoever is right.
6. **Two-round movement rule.** After each round, note whether either side changed any claim. Zero movement across 2 consecutive rounds means the gap is values or incentives, not information; further rounds add heat. Stop and record (`deadlock.md`).
7. **Converge to one design, never the average.** Compromise test: does the merged option still satisfy each side's original loss function? A blend of two coherent designs is usually incoherent. If the test fails, pick one design whole and record the losing objection with a revisit trigger.

## Collaborate vs Delegate vs Solo

Run these checks in order; first hit wins. Misrouting symptoms and hybrid sequences: `vs-delegate.md`.

1. Is the question settled knowledge (documented convention, prior decision, known fact)? → Solo, cite the source — check the decision log first. Collaboration on settled questions is lens theater.
2. Undo cost under `solo_undo_threshold` and blast radius limited to you? → Solo, ship, observe.
3. Can you write acceptance criteria a competent executor could verify without you? → Delegate.
4. Can the exchange surprise you (Rule 1)? → Collaborate, one counterpart.
5. None of the above (unclear criteria AND predictable counterpart)? → The task is underspecified; go get missing information first. Collaboration cannot substitute for facts neither party has.

## Counterpart Selection

One counterpart per exchange (default). Add a second only if round one surfaced a new dimension neither of you can judge. Full catalog with loss functions and recruiting guidance: `counterparts.md`.

| Gap you have | Counterpart to adopt or recruit | What they attack |
|---|---|---|
| Untested assumptions | Adversarial reviewer | The 3 assumptions that, if false, kill the plan; not the wording |
| Feasibility optimism | Implementer | Every step you wrote as "then we just..." |
| Correct but possibly unusable | Least patient user | The first 10 seconds of contact with the artifact |
| Local optimum, stale frame | Outsider from an adjacent field | Why this is the problem at all, not how you solved it |
| Long-tail fragility | Maintainer at month 6 | What breaks when the author is gone and context is lost |
| Scope creep | Budget holder | What gets cut to fund each addition |

If simulating the counterpart yourself: state their loss function in one line before the round ("this person is paged at 3am when it breaks") and hold it for the whole round. Dropping the loss function mid-round reverts you to self-agreement.

## Running the Exchange

1. **Position first.** Decision + strongest reason + kill condition, written before the counterpart sees anything (Rule 5).
2. **Brief tightly.** Context in one paragraph, your position, and ONE falsifiable question. "Any thoughts?" is banned: vague briefs return vague critique and burn the budget. Good: "Does assumption B survive a 10x traffic spike?" Bad: "Is this architecture okay?" Context dosing and question bank: `briefing.md`.
3. **Round structure.** Counterpart challenges → you restate their point until they would sign it (steelman check) → then respond. Rebutting a point you cannot restate means you rebutted a strawman.
4. **Track movement.** After each round, one line: what changed. Feeds Rule 6.
5. **Stop when:** your position changed and stabilized; OR 2 rounds passed with zero movement; OR the final round ends. Hard cap `round_cap` rounds (default 3).
6. **Converge.** Emit three items: the decision, the strongest surviving objection, and the trigger condition that reopens the question ("revisit if latency exceeds 200ms in production"). A convergence without a surviving objection means the exchange found nothing; say so explicitly rather than inventing one. Record per `decision-log.md` when `log_decisions` is on.

## Output Gates

Before emitting the converged result, verify:

- Position was written before the exchange started, with a kill condition
- The counterpart's response could have surprised me (if not, why did I run this?)
- The brief contained one falsifiable question, not an open invitation
- The result is one whole design, not an average of two
- The artifact names the surviving objection and a concrete revisit trigger
- The record landed in the decision log or the user's record convention, or skipping it was deliberate

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Sock-puppet counterpart | You unconsciously select for agreement; the exchange confirms, never tests | Pick the lens that loses if you are wrong (Rule 4) |
| "Thoughts?" briefing | Open prompts return politeness and generalities; budget spent, zero information | One falsifiable question per brief (`briefing.md`) |
| Averaging two designs | Coherence lives in the whole; the midpoint of two coherent designs satisfies neither loss function | Pick one whole; record the losing objection |
| Validation disguised as collaboration | You already decided; the exchange is a rubber stamp and the counterpart senses it | If no kill condition exists, skip the exchange and own the decision |
| Infinite rounds | Past 2 no-movement rounds the gap is values, not information; rounds add heat | Stop, record, escalate only if blocking (`deadlock.md`) |
| Same-information counterpart | Same inputs produce same blind spots regardless of role labels | Give them different data or a different loss function |
| Collaborating on settled questions | Re-litigating documented decisions burns trust and budget | Solo with a citation; reopen only via the recorded revisit trigger |
| Dropping the simulated loss function | Mid-round you drift back to your own incentives and agree with yourself | Re-read the one-line loss function at the start of each round |

## Where Experts Disagree

- **Anchored vs blind first pass.** Showing your position first speeds the attack but anchors the counterpart; a blind pass costs a round but yields an independent read. Default: anchored for adversarial review (the position IS the target), blind for second opinions (`second-opinions.md`).
- **Disagree-and-commit vs consensus.** Consensus only for decisions that need every party's sustained effort to survive; everywhere else a named owner decides and dissent is recorded. Waiting for consensus on reversible calls is the more common failure mode.
- **Pairing vs review.** Review scales and leaves a written trail; pairing transfers context and catches design errors before they are typed. The boundary is ambiguity: spec-able work gets review, unspec-able work gets pairing (`pairing.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/collaborate (install if the user confirms):
- `delegate` — the task has writable acceptance criteria; route it to a sub-agent instead of discussing it
- `diverge` — you need many parallel viewpoints generated before any of them is worth an exchange
- `six-thinking-hats` — structured solo rotation through fixed lenses when no real counterpart is available
- `brainstorm` — you need volume of options, not critique of one

## Feedback

- If useful, star it: https://clawic.com/skills/collaborate
- Latest version: https://clawic.com/skills/collaborate

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/collaborate.
