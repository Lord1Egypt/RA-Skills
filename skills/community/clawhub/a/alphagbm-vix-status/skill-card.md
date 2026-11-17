## Description:

Provides current VIX status with a five-tier fear classification, one-year context, and options-selling strategy hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent workflows use this skill to translate a market-wide VIX reading into a concise volatility backdrop for options-selling context. The output supports situational awareness and should be treated as informational market context, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading-oriented strategy hints may be mistaken for personalized investment advice.

Mitigation: Treat outputs as informational market context and verify suitability, position sizing, and risk limits before making any trade.

Risk: Stale or delayed VIX data can mislead timing-sensitive trading decisions.

Mitigation: Check the returned timestamp and confirm current market data freshness before using the result in a trading workflow.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-vix-status)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown or text summary with structured JSON fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No user parameters; includes VIX value, tier, color, bilingual label, strategy hint, one-year percentile, one-year mean, and tier distribution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
