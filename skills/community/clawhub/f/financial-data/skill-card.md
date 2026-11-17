## Description:

Query real-time and historical financial data across equities and crypto, including prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisapay](https://clawhub.ai/user/aisapay)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent builders use this skill to retrieve stock and cryptocurrency data from AIsa for market research, reporting, portfolio checks, and screening workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send tickers, date ranges, screener filters, and the AISA_API_KEY to api.aisa.one.

Mitigation: Use the skill only for intended AIsa market-data lookups and avoid submitting sensitive portfolio context beyond the query fields needed.

Risk: Automated or broad query loops may consume paid AIsa credits.

Mitigation: Keep the API key scoped or rotatable if supported and review workflows before running high-volume queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aisapay/skills/financial-data)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl or python3 and an AISA_API_KEY; API responses may include usage cost and credits remaining.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
