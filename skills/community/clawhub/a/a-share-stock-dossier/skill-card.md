## Description:

Analyzes A-share stocks and portfolios through evidence-first analyst reports that combine structured quote data, web research, source ranking, and explicit portfolio actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t-atlas](https://clawhub.ai/user/t-atlas)

### License/Terms of Use:


## Use Case:

Traders, analysts, and portfolio reviewers use this skill to assemble traceable A-share stock or portfolio dossiers with a retrieval log, structured market baseline, stock-by-stock evidence cards, and scenario-based actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce trading-style action suggestions that may be mistaken for financial advice.

Mitigation: Treat outputs as research support, verify conclusions against current official disclosures and market data, and preserve uncertainty notes in the report.

Risk: Requested stock symbols, searches, and related context may be sent to public web, Eastmoney, or Tencent market-data services.

Mitigation: Avoid submitting sensitive portfolio details unless external data sharing is acceptable for the intended use.

Risk: A-share quote snapshots and intraday market conditions can change quickly.

Mitigation: Refresh structured quote and kline data near the time of use and keep timestamps visible in the retrieval log.

## Reference(s):

- [Eastmoney Core Fields](references/eastmoney-fields.md)
- [Report Template](references/report-template.md)
- [Search Depth Protocol](references/search-depth-protocol.md)
- [Source Checklist](references/source-checklist.md)
- [Eastmoney quote API](https://push2.eastmoney.com/api/qt/ulist.np/get)
- [Tencent fqkline API](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with retrieval log, structured market-data summary, evidence cards, portfolio tiers, and scenario-based action guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a long-form analyst report unless the user asks for a shorter summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
