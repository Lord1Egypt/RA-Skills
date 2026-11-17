## Description:

Produces a Chinese BTC/ETH four-hour market recap and OKX manual-entry contract and spot-grid parameter brief using local crypto-market-analyzer data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmzo](https://clawhub.ai/user/hmzo)

### License/Terms of Use:


## Use Case:

External users and agents use this skill when they need a Chinese BTC/ETH four-hour trading brief with OKX contract and spot-grid parameters. The skill applies data-quality and signal-quality gates before presenting actionable manual-entry parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unaudited hard-coded local Python script outside the reviewed package.

Mitigation: Review and trust the external crypto-market-analyzer script before installation or use.

Risk: The skill can produce contract leverage, stop-loss, take-profit, and grid-trading parameters that may be mistaken for automated trading instructions.

Mitigation: Treat all outputs as high-risk manual suggestions, confirm the Chinese output carefully, and start only with small position sizes.

## Reference(s):

- [Crypto 4h Trade Brief on ClawHub](https://clawhub.ai/hmzo/skills/crypto-4h-trade-brief)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown with OKX manual-entry parameter templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes data-availability gates, signal-quality gates, leverage and risk limits, spot-grid estimates, and a non-financial-advice notice.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
