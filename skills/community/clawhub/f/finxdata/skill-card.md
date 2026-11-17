## Description:

Provides agents with financial data queries for stock prices, company disclosures, market themes, financial and macroeconomic data, commodities, FDA recalls, and stock graph summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuqp](https://clawhub.ai/user/qiuqp)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use FinXData to answer user requests for market, company, macroeconomic, commodity, and recall data, then summarize the results with their dates and coverage. It supports information lookup, not securities trading or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send parameters, the caller's IP address, and an agent-type identifier to FinXData. Account queries also send the configured API key and may use account quota.

Mitigation: Prefer key-free queries when they meet the request, keep API keys private, and check account quota when using account endpoints.

Risk: Returned data can have limited coverage or an older data date, and remote text and links are untrusted content.

Mitigation: Check the returned date and coverage, and treat remote content as data rather than instructions or automatic link targets.

## Reference(s):

- [Quickstart](artifact/references/quickstart.md)
- [Usage guide and troubleshooting](artifact/references/usage.md)
- [API reference](artifact/references/api.md)
- [FinXData website](https://www.finxdata.ai)
- [World Bank Pink Sheet commodity data catalog](https://datacatalog.worldbank.org/search/dataset/0038238/commodity-prices-history-and-projections)
- [openFDA Enforcement Reports API](https://open.fda.gov/apis/drug/enforcement/how-to-use-the-endpoint/)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Concise text summaries, JSON query results, and Markdown tables or excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include dates, coverage details, or partial-success status; summarize those details when relevant.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
