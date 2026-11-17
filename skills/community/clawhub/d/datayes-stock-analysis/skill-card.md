## Description:

Generates Chinese-language individual stock research reports using Datayes MCP data across company profile, market trends, business and financial analysis, valuation, fund flow, technical indicators, and a summarized conclusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datayes](https://clawhub.ai/user/datayes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request structured Chinese-language stock analysis reports for a named security. The skill gathers Datayes MCP market, company, financial, shareholder, and event data, validates the results, and presents informational analysis rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock analysis output may be mistaken for personalized investment advice.

Mitigation: Keep the report framed as informational analysis, retain the disclaimer, and require users to make independent investment decisions.

Risk: Market and financial data can be stale, incomplete, or incorrect.

Mitigation: Verify important figures independently, include data cutoff dates, and run the provided validation checklist before relying on the report.

## Reference(s):

- [MCP Tools](references/mcp-tools.md)
- [Stock Analysis Data Validation](references/stock-analysis-data-validation.md)
- [Stock Analysis Framework](references/stock-analysis-framework.md)
- [Stock Analysis Report Template](references/stock-analysis-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown stock analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tabular metrics, a data cutoff date, validation checks, a summarized score, risk notes, follow-up focus areas, and a disclaimer that the report is not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
