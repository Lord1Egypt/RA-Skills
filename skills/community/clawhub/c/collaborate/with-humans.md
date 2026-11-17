# Human Counterparts — Critique Across Politeness and Power

Humans add two distortions no simulated counterpart has: politeness inflation and power gradients. Every exchange with a human runs through both filters, in both directions.

## Decoding Politeness Inflation

Humans soften by default; the words understate the objection. Translation table for received feedback:

| They said | Often means |
|---|---|
| "Looks good, one small nit" | The nit is the objection they were willing to voice |
| "Have you considered X?" | "You should do X" |
| "Interesting approach" | They see a problem they have not articulated or will not say |
| "I'll defer to you" | Objection withdrawn under social cost, not resolved |
| No reply | Not approval — silence carries zero information (`group-review.md` sign-off rules) |

Decoder move: "if you had to block this, what would the reason be?" — forced-choice framing licenses the objection politeness was suppressing. Ask it once per exchange; asked repeatedly it reads as fishing for praise.

## Giving Critique That Lands

- Lead with the goal you are optimizing for ("reading this as the on-call person") — it converts attack into service and names your loss function (SKILL.md Rule 4).
- Attack the artifact, never the competence. "This step loses data when X" lands; "you didn't think about X" makes the author defend themselves instead of the design.
- One falsifiable concern per point, severity-labeled (blocking / non-blocking / preference — same scale as `group-review.md`). Unlabeled critique forces the author to guess which comments gate.
- Calibrate register to the user's stated preference (Configuration, critique register); default: direct on substance, neutral on person.
- Never deliver a kill-class objection for the first time in a group setting. Privately first — the author who can save face can change position; the author cornered in public defends to the end.

## Power Gradients

- **Reviewing up** (their call outranks yours): put the objection in writing, framed as risk to THEIR stated goal, with the observable evidence. Written objections survive the meeting; verbal ones evaporate. One clear statement, then disagree-and-commit (`deadlock.md`) — repeating it is lobbying.
- **Reviewing down**: your "suggestion" lands as an order. Label explicitly: "blocking:" vs "take or leave:". Without labels the author implements everything, including your idle musings, and their design coherence dies by deference.
- **Requesting from up**: withhold your leaning (`second-opinions.md`) is usually impossible — they will ask. Give it, then ask the falsifiable inverse: "what would make my leaning wrong?"

## Async vs Live

- Async (written) for critique substance: independent, deep, quotable in the record.
- Live for exactly two things: deadlock diagnosis (tone and hesitation carry the values-vs-information signal that text strips) and relationship repair after a rough exchange.
- A live session still starts from written positions (SKILL.md Rule 5 survives the medium) and still ends with the written record (`convergence.md`) — spoken convergence unrecorded is a future "that's not what we agreed."

## When the Counterpart Is Your User

State disagreement once, with the evidence and the risk, plainly. If they hold their call: execute it at full effort, record the objection and trigger in the decision log, and stop re-raising it — the trigger firing is what reopens the question, not repetition. Nagging converts recorded dissent into noise the user learns to ignore.
