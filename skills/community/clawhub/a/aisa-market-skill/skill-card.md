## Description:

Query real-time and historical financial data across equities and crypto--prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to retrieve market data for equities and crypto, including prices, news, financial statements, analyst estimates, SEC filings, interest rates, and screeners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's API key and requested tickers, date ranges, and screener filters to AIsa.

Mitigation: Use a dedicated AIsa API key, limit its credit exposure where possible, and avoid submitting sensitive portfolio or strategy details in queries.

Risk: API calls may consume paid credits.

Mitigation: Review commands before execution and monitor returned usage cost and credits remaining.

## Reference(s):

- [AIsa API Reference](https://docs.aisa.one/reference/)
- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/bowen-dotcom/skills/aisa-market-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python command examples, plus JSON responses from API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to the AIsa API; API responses may include usage cost and credits remaining.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
