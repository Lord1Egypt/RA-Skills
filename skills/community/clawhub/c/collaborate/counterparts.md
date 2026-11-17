# Counterpart Catalog — Loss Functions and Simulation Discipline

The selection rule (SKILL.md Rule 4): the counterpart must differ from you in loss function or information, ideally both. Same incentives + same inputs = echo with extra steps. This file is the full catalog; the six most common gaps are in SKILL.md Counterpart Selection.

## Catalog

One line of loss function is the whole persona. State it before the round; everything else follows from it.

| Counterpart | Loss function (one line) | What they attack | Opening question |
|---|---|---|---|
| Adversarial reviewer | Pays when an untested assumption ships | The 3 load-bearing assumptions | "Which assumption, if false, kills this?" |
| Implementer | Owns every "then we just..." step | Feasibility gaps, hidden integration work | "Walk me through step 4 concretely" |
| Maintainer at month 6 | On-call when the author is gone | Undocumented decisions, fragile coupling | "What breaks first when context is lost?" |
| Least patient user | Bails at the first friction | The first 10 seconds of contact | "Why would I keep reading?" |
| On-call operator | Paged at 3am when it breaks | Observability, failure modes, rollback path | "How do I know it's broken, and how do I undo it?" |
| Security auditor | Blamed for the breach | Trust boundaries, data flows, defaults | "What does an attacker do with this?" |
| Budget holder | Funds every addition from a fixed pot | Scope creep, unpriced maintenance | "What gets cut to pay for this?" |
| Adjacent-field outsider | Nothing invested in the current frame | Why this is the problem at all | "What are you actually trying to cause?" |
| Newcomer | Punished by every unexplained term | Curse of knowledge, missing prerequisites | "What must I already know for this to make sense?" |
| Compliance/legal lens | Liable for the promise the artifact makes | Overclaims, data handling, irreversible commitments | "What are we promising, and to whom?" |
| Churned customer | Already left once for a reason | The gap between pitch and lived experience | "What made me leave, and does this fix it?" |
| Competitor | Wins when you misallocate | Differentiation, effort spent on parity features | "Which part of this would I be glad you built?" |

## Choosing

- Match the counterpart to the gap, not to availability. The convenient counterpart with your incentives is worse than a simulated one with opposite incentives.
- Recruiting real people: prefer whoever owns the consequence (the actual on-call, the actual budget holder). Nearest person with different incentives beats the farthest expert.
- One counterpart per exchange (SKILL.md). Two lenses you genuinely need → two sequential rounds, not one blended persona. Blended personas average into mush — the same failure as averaging two designs.

## Simulation Discipline

When no real counterpart is reachable (`counterpart_mode` resolves to simulate):

1. Write the loss function in one line BEFORE reading your own position again.
2. Re-read that line at the start of every round; dropping it mid-round reverts you to self-agreement (SKILL.md Traps).
3. Produce the counterpart's strongest attack, not their probable politeness. Simulated counterparts have no social cost — use that.
4. Signs the simulation collapsed: critiques turn abstract ("consider edge cases"), you start agreeing within the same paragraph, the attack targets wording. Any sign → restate the loss function and redo the round.
5. Honest ceiling: a simulation shares your information by construction. It can vary the loss function, never the inputs. When the gap you need is information (domain facts, user reality), simulation cannot close it — recruit, or go get the facts first (SKILL.md routing check 5).

## Anti-Patterns

- Briefing the counterpart with your conclusion embedded — you built a sock puppet with extra steps.
- Picking the lens that mirrors your own bias (the performance hawk reviewing your performance-motivated rewrite).
- Rotating through many personas in one sitting — that is divergence; route to `diverge` and return with the one lens that bit.
- Ignoring the critique that landed because it came from the "wrong" persona. The attack's validity does not depend on the mask.
