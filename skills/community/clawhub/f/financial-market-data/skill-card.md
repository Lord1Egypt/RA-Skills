## Description:

Provides a unified interface and examples for retrieving financial market data from TickFlow, AkShare, BaoStock, pytdx, Tonghuashun, and Eastmoney.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjdenglun](https://clawhub.ai/user/bjdenglun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to add market-data retrieval workflows for equities, futures, ETFs, sectors, financials, fund flows, and macroeconomic indicators, with fallback examples across several data providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts external financial-data providers with requested symbols.

Mitigation: Install only when this network behavior is acceptable for the intended symbols and environment.

Risk: The release evidence reports an embedded reusable Eastmoney API key.

Mitigation: Treat the key as exposed, replace it with a user-provided secret before use, and avoid committing replacement secrets.

Risk: The security evidence identifies data-quality and dependency risks.

Mitigation: Prefer pinned dependencies or a lockfile, and verify intraday data correctness before relying on results for trading, alerts, or financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bjdenglun/skills/financial-market-data)
- [Eastmoney MX API documentation](https://openapi.eastmoney.com/mx/v1/api-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code snippets, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced Python helpers can return pandas DataFrames, lists, and JSON-like dictionaries from external financial-data providers.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
