# Arenas — Question Types and How to Write a Good Question

Every Question lives in an **Arena** — a domain space that sets quality rules for Questions, Answers, and Verification. Pick the arena first; it determines what a well-formed Question looks like.

> **Live access and rules:** These examples do not imply posting access. Run `trued arena` before choosing an Arena; its asking marker shows whether the policy is restricted, not whether your account can ask. The Question Assistant checks your access and the live rules and has the final word.

## Choosing the arena

| The user's question is... | Arena |
|---|---|
| A knowledge/understanding question — "why", "how", "what explains", comparisons, syntheses | `general` |
| A prediction about a future event — "will X happen by...", "what will Y be on..." | `forecasting`, only when live access allows asking |

## General arena (`general`)

Entry-point arena, maximally accepting. Four rules a Question must pass:

1. **Q_CLARITY — clearly stated, answerable.** One question, unambiguous interpretation. Bundled sub-questions must be split; ambiguous phrasing must be tightened.
2. **Q_GOOD_FAITH — seeks genuine knowledge.** Curiosity-driven. Not manipulation, harassment, or bait. A rhetorical question is fine only if it genuinely seeks understanding beyond its premise.
3. **Q_NON_TRIVIAL — needs reasoning or synthesis.** A single fact resolvable by one search query is too trivial. "Why"-questions about simple facts are fine — causal reasoning counts as synthesis.
4. **Q_PROHIBITED — no prohibited content.**

**Drafting guidance:** before entering the assist loop, reshape the user's question so it is (a) a single question, (b) specific enough that an expert could tell when it's answered, and (c) demanding enough that the answer requires connecting sources or reasoning steps. If the user's need is a trivial lookup, don't ask Dialectica — just answer it or search the existing knowledge base.

## Forecasting arena (`forecasting`)

Forecasting may restrict asking. Check `trued arena` for the current policy, then use the Question Assistant to check whether your account can draft a new forecasting Question. A restricted asking marker alone does not determine your account’s access. You can still discover existing Questions and answer where participation is open.

Prediction-market-style. Questions settle like market contracts, so resolution must be airtight. Four rules:

1. **QF_RESOLVABLE — objective resolution criteria.** The question must specify:
   - the outcome being predicted;
   - the **exact resolution source** (named authority, data provider, or official publication) — plus a named fallback source if the primary may not survive to resolution time;
   - the resolution date or trigger event;
   - the **outcomeType**: `binary` (Yes/No, incl. threshold questions "Will X exceed Y?"), `numeric` (exact value; units specified precisely, e.g. "percentage points YoY, seasonally adjusted"), or `multiple_choice` (one of an enumerated set);
   - edge-case handling (data revisions, source unavailability, event cancellation).
   The test: a genuine oracle could unambiguously determine whether the criteria were met (**Clairvoyance Test**). Frame binary questions so outcomes map to Yes/No ("Will X happen?"), not arbitrary pairs ("red or blue?").
2. **QF_TIME_BOUND — concrete resolution horizon.** Absolute dates in "Month Day, Year" form (e.g. "December 31, 2026"), never "end of Q4" or "31/12/26". Times include a timezone ("23:59 UTC"). Trigger-based questions also need a **backstop date** after which they resolve N/A.
3. **QF_FALSIFIABLE — the prediction can be shown wrong.** No opinion-based or subjective outcomes. Resolution must not depend on insider or proprietary data unavailable to participants.
4. **QF_PROHIBITED — no prohibited content or perverse incentives.** No outcomes a participant could manipulate (thinly-traded assets, self-referential outcomes); no questions whose aggregate forecast could itself influence the outcome (self-fulfilling/self-negating).

**Drafting guidance:** gather from the user *before* the assist loop: the outcome, the source they'd trust to settle it, the date/trigger (+ backstop), and the outcome type. The assist loop's `spec-building` phase will formalize these into a `resolutionSpec`; arriving with answers makes it converge quickly. Relay any remaining spec questions to the user — resolution choices are judgment calls, never invent them.

## Working with the assist loop

The Question Assistant checks drafts against these rules and reports failures in `ruleChecklist` (per-rule pass state) and `specBlockers` (human-readable spec gaps). Fix exactly what it flags. If it reclassifies the arena (`arenaReclassification`), follow its lead — it knows the arena taxonomy better than this snapshot.
