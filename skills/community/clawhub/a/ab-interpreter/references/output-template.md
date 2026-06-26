# A/B Test Readout Template

Every readout has four blocks. Keep each block short, numbered, and scannable so a skeptical executive can read it in under two minutes.

## Block 1: Verdict

One line. Ship, Kill, Extend, or Redesign. Followed by the single most important reason.

- **Ship** — Significant, above MDE, guardrails intact, segments consistent, novelty decay acceptable
- **Kill** — Significant but regresses a guardrail, or contradicts key segment, or below MDE
- **Extend** — Directionally positive but underpowered or too short
- **Redesign** — Flat or mixed result that suggests the hypothesis was wrong

Example: "Ship. Variant B beats control by 4.1% on conversion with a 95% CI of +1.8% to +6.5%; guardrails intact; all segments align."

## Block 2: Statistics

Report the numbers a peer reviewer would ask for:

- Observed lift (absolute and relative)
- 95% confidence interval on the lift
- p-value and the test used (two-proportion z, Welch's t, chi-squared)
- Sample size per arm and the power actually achieved
- Minimum detectable effect set before the test began
- Duration and whether it covered two full business cycles

## Block 3: Risk

List anything that would give a skeptic pause:

- Sample ratio mismatch (observed vs. planned split)
- Segments that contradict the aggregate direction
- Guardrail regressions, even if not statistically significant
- Novelty risk if lift was front-loaded
- Seasonality, promo overlap, or tracking outages during the window
- External factors: competitor moves, press coverage, paid media spikes

## Block 4: Next step

One concrete action. Never end a readout without one.

Patterns:
- "Roll out to 100% over 48 hours; monitor AOV and refund rate weekly for four weeks"
- "Extend the test to 21 days to narrow the CI below the MDE"
- "Redesign the hypothesis around [specific segment] where lift was concentrated"
- "Kill the variant; queue a follow-up test on [revised hypothesis]"

## Tone notes

Avoid hedging language that obscures the call. "Potentially a modest lift" is not a verdict. "Ship" and "Kill" are. If you cannot commit to a verdict, say "Extend" and state the exact trigger for a re-read.
