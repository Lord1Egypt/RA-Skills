## Description:

China fund and stock data MCP server for querying fund valuation, NAV, holdings, manager information, stock and index quotes, market capital flow, sector rankings, northbound capital, and local portfolio profit calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallke](https://clawhub.ai/user/smallke)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this MCP server to let an agent retrieve China-market fund, stock, index, capital-flow, and portfolio summary data without an API key. It can also store local fund holdings and reminders for recurring portfolio or market updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved portfolio holdings and reminder data can include sensitive personal finance information.

Mitigation: Install only when local persistence is acceptable, restrict access to the data directory, and remove saved holdings or reminders when they are no longer needed.

Risk: Screenshot-based portfolio import may expose brokerage or payment-app account details if users upload unredacted images.

Mitigation: Avoid uploading unredacted financial screenshots and crop or redact unrelated account, identity, and transaction details before OCR import.

Risk: Fund and stock identifiers are sent to third-party market-data APIs.

Mitigation: Use the skill only with identifiers that may be shared with those data providers and review applicable provider terms for the deployment context.

Risk: Automatic reminders and custom reminder text can surface saved user content as agent-facing instructions.

Mitigation: Review or disable the reminder workflow before use, and keep custom reminder messages short, factual, and free of operational instructions.

Risk: Portfolio outputs may include add-position, reduce-position, or profit-taking suggestions that could be mistaken for regulated investment advice.

Mitigation: Treat all analysis as generic informational output, verify market data independently, and consult a qualified professional before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallke/skills/cn-funds-mcp)
- [EastMoney data source](https://www.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [MCP tool responses as text containing JSON market data, portfolio summaries, reminder prompts, or concise user-facing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses third-party market-data endpoints and local JSON files for portfolio and reminder state.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
