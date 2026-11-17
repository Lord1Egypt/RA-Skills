# Adversarial Review — Attacking a Plan Before Reality Does

For plans and designs you are about to commit to. The counterpart's job is to make the plan fail on paper, where failure is cheap. Anchored pass: the counterpart sees your written position — the position IS the target.

## Extract the Load-Bearing Assumptions

Before any attack, list what the plan silently assumes. Test for load-bearing: "if this is false, does the plan survive?" Keep only the ones where the answer is no; attack the top 3 (SKILL.md Quick Reference). Attacking more than 3 in one round produces a gish gallop the author cannot process.

Assumption taxonomy — scan all five, plans rarely fail where the author looked:

| Type | The silent claim | Classic miss |
|---|---|---|
| Demand | Someone wants this enough to change behavior | Built for a stated preference, not an observed one |
| Feasibility | We can build it with what we have | The one step written as "then we just..." |
| Capacity | We can afford to run and maintain it | Launch cost budgeted, month-6 maintenance not |
| Timing | The window stays open while we build | Dependency ships late; the plan has no slack consumer |
| Dependency | External parties behave as assumed | API limits, approval chains, a vendor's roadmap |

## The Pre-Mortem

Strongest single move when the author is confident: "It is 6 months from now and this plan failed. Write the story of how." A narrative forces concrete mechanisms; a risk list lets everyone nod at abstractions. Run it before the attack round — the failure story usually names the assumption worth attacking first.

## Attack Rules

- Attack the assumption, never the wording or the author. "This paragraph is unclear" is copyediting, not review.
- Every attack names the observable evidence that would confirm it ("if demand is fake, the waitlist converts under X"). An attack with no observable consequence is a vibe.
- Severity-label every attack: **kill** (plan dies), **wound** (plan needs surgery), **cosmetic** (note and move on). Only kill-class attacks justify another round.
- The author steelmans before rebutting (SKILL.md Running the Exchange step 3). Real-time defense is the review's failure mode: the author leaves having practiced their pitch, not having tested it.

## After the Attack: Cheapest Test First

For each surviving kill-class attack, name the cheapest experiment that settles it before commitment — a call, a prototype, a query on existing data. Order: cheapest-to-test first, not scariest first. A plan that commits with an untested kill-class assumption should say so in its decision record as the revisit trigger.

Output of the review — one table: `assumption → attack → observable evidence → cheapest test`. Plus the standard convergence record (`convergence.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Twenty minor objections | Volume reads as rigor but buries the two that matter; author fixes commas | Cap at 3 attacks, severity-labeled |
| Attacking the presentation | The plan improves as a document and dies as a plan | Attack only load-bearing assumptions |
| Author defends in real time | Review becomes a debate; positions harden | Steelman first; respond after restating |
| Reviewer proposes their own plan | Now two plans need review and the round is over | Attacks only; alternatives belong to a second-opinions exchange |
| Skipping the pre-mortem on "obvious" plans | Confidence is exactly the symptom that triggers this file | Run it; it costs minutes |
