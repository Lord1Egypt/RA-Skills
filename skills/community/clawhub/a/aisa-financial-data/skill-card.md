## Description:

Query real-time and historical financial data across equities and crypto, including prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisapay](https://clawhub.ai/user/aisapay)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent builders use this skill to retrieve equity and cryptocurrency market data for portfolio monitoring, investment research, screening, alerts, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API bearer token could be exposed if authenticated Python client requests follow redirects to a different origin.

Mitigation: Use a limited, rotatable API key and restrict network egress to the intended AIsa API host; the publisher should prevent authenticated cross-origin redirects.

Risk: Financial queries and screener filters may contain sensitive portfolio, personal, or account-related information.

Mitigation: Avoid sending sensitive personal or account data in query fields and review requests before execution.

Risk: API usage may consume paid credits.

Mitigation: Monitor credit usage and use scoped keys or account controls where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisapay/skills/aisa-financial-data)
- [Publisher profile](https://clawhub.ai/user/aisapay)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and Python command examples, plus JSON responses from the API client.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, curl, and an AISA_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
