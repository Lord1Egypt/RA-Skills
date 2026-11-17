## Description:

The Hunter: Professional Binance Trading Skill. Features AI market analysis, auto-risk calculation, and 125x leverage support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tetravad](https://clawhub.ai/user/tetravad)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for Binance market analysis, trading guidance, credential setup steps, and spot or futures API command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents and users direct live trading authority with weak safety boundaries.

Mitigation: Review the skill carefully before installing and use read-only or testnet Binance keys unless live trading is explicitly intended.

Risk: Credential exposure or overly broad Binance API permissions could enable unintended account actions.

Mitigation: Disable withdrawal permission, apply IP restrictions where possible, and protect any credential file with restrictive permissions.

Risk: Production order and leverage commands could execute high-risk trades if run without review.

Mitigation: Require explicit per-trade approval before running production order, stop-loss, take-profit, or leverage commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tetravad/skills/binance-hunter)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Binance Testnet](https://testnet.binance.vision/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live Binance API command examples and a JSON market-analysis script output.]

## Skill Version(s):

1.0.0 (source: package.json, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
