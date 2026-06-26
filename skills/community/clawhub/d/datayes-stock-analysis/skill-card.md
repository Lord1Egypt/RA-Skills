## Description: <br>
Datayes Stock Analysis helps agents produce structured single-stock research reports using Datayes market, financial, ownership, event, and technical-analysis data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datayes](https://clawhub.ai/user/datayes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate a structured stock research report for a named equity, covering company profile, price action, operations, valuation, capital flows, technical indicators, and a non-advisory conclusion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial outputs may be mistaken for personalized investment advice or may include buy/sell-style technical signals. <br>
Mitigation: Treat the report as objective research only, keep the disclaimer, and require users to make independent investment decisions. <br>
Risk: Market and financial data can be stale, incomplete, or unavailable for some securities or markets. <br>
Mitigation: Follow the included data validation checklist, cite the data cutoff date, and mark unavailable or unsupported indicators clearly. <br>


## Reference(s): <br>
- [Datayes Stock Analysis ClawHub page](https://clawhub.ai/datayes/datayes-stock-analysis) <br>
- [MCP tool list](references/mcp-tools.md) <br>
- [Stock analysis data validation checklist](references/stock-analysis-data-validation.md) <br>
- [Stock analysis framework](references/stock-analysis-framework.md) <br>
- [Stock analysis report template](references/stock-analysis-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown stock analysis report with tables, data cutoff, and disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Datayes MCP tools; technical indicators are skipped for unsupported markets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
