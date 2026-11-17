## Description:

Provides IV Rank and IV Percentile analysis that compares current implied volatility with a 252-day history and returns volatility context, metrics, and trading-signal guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate whether a ticker's implied volatility is high or low relative to recent history and to frame options-volatility strategy decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals may be mistaken for personalized financial advice.

Mitigation: Treat outputs as informational options-volatility context and independently confirm any trade decision.

Risk: Broad volatility questions may receive buy- or sell-premium strategy suggestions.

Mitigation: Review strategy suggestions against the user's objectives, risk tolerance, and current market conditions before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-iv-rank)
- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API base URL](https://alphagbm.zeabur.app)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown or JSON volatility metrics with trading-signal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IV rank, IV percentile, IV history, historical-volatility comparisons, volatility risk premium, zone classification, and suggested options strategies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
