## Description:

Fetches A-share, Hong Kong, and U.S. stock market data with AkShare, including quotes, history, intraday data, financials, shareholder data, fund flows, sector data, margin data, IPO data, valuation metrics, and ESG ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengr](https://clawhub.ai/user/zhengr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to retrieve public stock market and company data for A-share, Hong Kong, and U.S. equities. It supports market lookup, historical data collection, financial analysis, fund-flow review, sector review, and related stock data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Python code that imports AkShare and contacts public financial data providers.

Mitigation: Review generated Python snippets and shell commands before execution, and run them in an environment where outbound data-provider access is acceptable.

Risk: Returned market data may be delayed, incomplete, rate-limited, or temporarily unavailable from upstream providers.

Mitigation: Check timestamps and data-source notes before relying on results, and avoid excessive polling of provider endpoints.

Risk: Financial data may be misused as investment advice.

Mitigation: Treat outputs as market data for analysis only and require appropriate human review before making trading or investment decisions.

Risk: Optional provider tokens or account credentials could be exposed if pasted into prompts or scripts.

Mitigation: Keep tokens private, avoid hard-coding credentials, and use environment-level secret handling when provider authentication is required.

## Reference(s):

- [AkShare stock API reference](references/api_reference.md)
- [AkShare Stock Data Pro release page](https://clawhub.ai/zhengr/skills/akshare-stock-pro)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; command results are CSV or JSON-like tabular text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+ with AkShare installed; returned data should be treated as market data, not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
