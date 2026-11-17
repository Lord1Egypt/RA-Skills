## Description:

Integrates prediction market data from Polymarket with options analysis to surface mispricing signals between event probabilities and options-implied probabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and traders use this skill to compare prediction-market event probabilities with options-implied probabilities and identify potential event-driven options mispricing signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce speculative trading guidance for options and event-driven markets, where losses can happen quickly.

Mitigation: Treat outputs as informational research and independently verify market data, assumptions, and risk exposure before acting.

Risk: Prediction-market and options-implied probabilities may diverge for reasons other than actionable mispricing.

Mitigation: Review the event mapping, confidence level, spread threshold, and historical-accuracy context before relying on any signal.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-polymarket)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and concise analysis with suggested options trades]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include probability comparisons, spread rankings, confidence indicators, historical-accuracy context, and trade suggestions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
