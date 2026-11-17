# Convergence — Landing the Decision and Its Record

An exchange that ends without these three items did not converge, it just stopped: the decision, the strongest surviving objection, the revisit trigger (SKILL.md Running the Exchange step 6).

## One Design, Whole

The compromise test (SKILL.md Rule 7): does the merged option still satisfy each side's original loss function? Run it on any blend before accepting it.

- Blends fail because coherence lives in the whole: half of design A's caching plus half of design B's consistency model satisfies neither's guarantees.
- Legitimate merges exist — when the designs differ in a separable dimension (A's storage layout + B's API surface, coupled by nothing). "Coupled by nothing" is the check; if changing one half forces rework in the other, they were not separable.
- When the test fails: pick one design whole. The losing design's strongest point becomes the surviving objection, not a bolt-on feature.

## The Surviving Objection

- It is the best argument against what you decided, stated so its author would sign it — steelman quality, not a strawman for the record.
- No surviving objection after a real exchange = the exchange found nothing; write exactly that. Inventing an objection to look rigorous poisons the log with fake signals.
- The objection is the revisit trigger's parent: a good trigger is "the condition under which the surviving objection turns out to be right."

## Revisit Trigger Quality

The trigger must be observable and thresholded — a condition someone can notice firing without re-reading the debate.

- Good: "revisit if latency exceeds 200ms in production" · "revisit when the team exceeds 10 people" · "revisit if the vendor deprecates the API".
- Bad: "revisit if it doesn't work out" (not observable) · "revisit in the future" (no threshold) · "revisit if problems arise" (everything qualifies, so nothing does).
- Date triggers are legitimate for decisions made under time pressure with thin evidence: "revisit at the next quarterly review" — the date substitutes for the metric you could not name.

## The Record

Fields and storage format: `decision-log.md`. Written by the decision owner, at convergence time — records reconstructed later inherit the winner's memory. Goes to `~/Clawic/data/collaborate/decisions.md` when `log_decisions` is on, or to the user's own convention (ADRs, repo docs — Configuration preference areas) when they have one; one home per decision, never both.

## Close the Loop With the Counterpart

Tell the counterpart what was decided and what their objection changed — even (especially) when the answer is "nothing, and here is why it still made the record." Counterparts who see their critique metabolized stay honest and available; counterparts who critique into a void start returning politeness. This one message is the cheapest investment in every future exchange.

## Reopening

- Legitimate: the recorded trigger fired; genuinely new information (not a re-weighting of known information); the decision owner changed and inherits the risk.
- Not legitimate: someone re-feels the losing position; a new person repeats the recorded objection without new evidence — answer with the record's citation, not a new exchange (SKILL.md Traps, settled questions).
- Reopened decisions get a fresh exchange and a new record that supersedes the old one (`decision-log.md` status rules); the old record stays — the history of reversals is itself decision data.
