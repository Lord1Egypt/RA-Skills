## Description:

Cryptocurrency market data and price alert monitoring tool based on CCXT. Supports multiple exchanges, real-time price tracking, and configurable price/volatility alerts. Use when the user needs to monitor crypto prices or set up trading alerts. Default exchange is Binance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to fetch cryptocurrency ticker, OHLCV, and order book data, monitor live prices, and manage local price or volatility alerts through a CCXT-based CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local CLI contacts cryptocurrency exchanges for public market data.

Mitigation: Install only if outbound requests to exchange APIs are acceptable for the target environment, and use explicit exchange selection where needed.

Risk: Alert settings are stored locally under ~/.config/crypto/alerts.json.

Mitigation: Review the local alert file before and after use, and avoid storing sensitive information in it.

Risk: Dependency installation guidance and the documented default exchange may not match runtime behavior.

Mitigation: Use a virtual environment with a pinned CCXT version, and pass --exchange explicitly until the default mismatch is fixed.

Risk: Advanced examples mention API key fields.

Mitigation: Do not put real API keys into example code, committed files, or this public market-data workflow.

## Reference(s):

- [CCXT Documentation](https://docs.ccxt.com/)
- [Supported Exchanges List](references/exchanges.md)
- [CCXT GitHub](https://github.com/ccxt/ccxt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local alert settings at ~/.config/crypto/alerts.json when alert commands are run.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
