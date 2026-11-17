## Description:

Query real-time and historical financial data across equities and crypto, including prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadevco](https://clawhub.ai/user/aisadevco)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to query AIsa market-data endpoints for equities, crypto, financial statements, analyst estimates, filings, insider activity, ownership, rates, and stock screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AIsa API keys and financial query details, including tickers, date ranges, and screener filters, are sent to api.aisa.one.

Mitigation: Use a dedicated revocable API key where possible and avoid sending account-specific or private portfolio details unless intended.

Risk: The skill performs authenticated market-data API calls that may consume paid credits.

Mitigation: Review query scope before execution and monitor response usage fields such as cost and credits remaining.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadevco/skills/aisa-financial-data-api)
- [Publisher profile](https://clawhub.ai/user/aisadevco)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl and Python command examples; CLI execution returns JSON from the AIsa API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to api.aisa.one.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
