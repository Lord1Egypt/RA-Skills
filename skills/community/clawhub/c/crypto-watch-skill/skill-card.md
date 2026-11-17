## Description:

Provides cryptocurrency and precious metals market data analysis with K-line data, funding rates, open interest, long/short ratios, liquidation data, option ratios, sentiment data, and technical indicators for assets such as Bitcoin, Ethereum, BNB, ZEC, SOL, and Gold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[burceasn](https://clawhub.ai/user/burceasn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve market data, calculate technical indicators, and prepare educational cryptocurrency or precious-metals analysis for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Leveraged trading outputs may be mistaken for personal financial advice.

Mitigation: Treat leverage, entry, stop-loss, and position-size outputs as educational analysis that requires human judgment before action.

Risk: The skill contacts public market-data APIs, so responses may fail or depend on stale, delayed, or incomplete upstream data.

Mitigation: Run the skill in a normal virtual environment with reviewed dependency versions and verify important results against current market sources.

Risk: Users may expose exchange credentials or authorize trading beyond the skill's intended scope.

Mitigation: Do not provide exchange API keys and do not let an agent trade, custody funds, or execute financial decisions based on this skill.

## Reference(s):

- [Technical Indicators Reference](references/INDICATORS.md)
- [Trading Strategy Guidelines](references/STRATEGY.md)
- [Crypto Technical Analysis Skill README](README.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON from CLI commands and Markdown guidance for analysis responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to public OKX and alternative.me market-data APIs; does not require exchange API keys.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
