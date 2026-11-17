## Description:

Provides stock, fund, futures, technical-indicator, sector-rotation, and portfolio-diagnosis analysis by guiding an agent to run the bundled AKShare-based CLI and return structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[429668385](https://clawhub.ai/user/429668385)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Chinese market data, calculate MA/MACD/RSI indicators, inspect representative sector or stock movement, and diagnose portfolio profit/loss and risk levels. It is intended for market-data analysis workflows, not as standalone investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes external requests to market-data endpoints and may send stock codes or portfolio details to third-party finance services.

Mitigation: Use only data the user is comfortable sharing, avoid sensitive portfolio details unless required, and run the skill in an isolated environment.

Risk: The security summary states that the documentation does not fully match the shipped CLI behavior.

Mitigation: Validate available CLI commands against the shipped script before relying on documented examples or exposing workflows to users.

Risk: Unpinned dependencies may change behavior over time.

Mitigation: Pin akshare, pandas, numpy, and requests versions before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/429668385/skills/akshare-stock-analysis)
- [Tencent Finance quote endpoint used by CLI](https://qt.gtimg.cn/q=)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market prices, technical indicators, portfolio profit/loss, risk labels, and error JSON from the CLI.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
