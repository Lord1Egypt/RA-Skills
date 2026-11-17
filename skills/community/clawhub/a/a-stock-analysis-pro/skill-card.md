## Description:

CN Stock Analysis Pro helps an agent produce Chinese A-share stock research reports by collecting public market, financial, capital-flow, event, and industry data and rendering an HTML report that can be exported to PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill-lib](https://clawhub.ai/user/bill-lib)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate Chinese-language A-share equity research reports from a stock code or stock name. It is intended for informational market analysis workflows, not for personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce reports that readers may treat as investment advice.

Mitigation: Keep the report disclaimer visible, present outputs as informational analysis, and require human review before using the report for financial decisions.

Risk: Real-time prices and financial metrics may be stale, unavailable, or inconsistent across public finance websites.

Mitigation: Use the skill's highest-priority real-time quote source as the price baseline, verify the report date and source freshness, and avoid replacing current prices with older search snippets.

Risk: Automated scenario probabilities, risk ratings, and target ranges may overstate certainty.

Mitigation: Review assumptions against the collected source data and require probabilities, catalysts, and risk ratings to be explicitly tied to observable triggers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bill-lib/skills/a-stock-analysis-pro)
- [Publisher profile](https://clawhub.ai/user/bill-lib)
- [analysis-prompts.md](references/analysis-prompts.md)
- [data-sources.md](references/data-sources.md)
- [report-template.md](references/report-template.md)
- [Eastmoney quote page](https://quote.eastmoney.com/{exchange}{stock_code}.html)
- [Sina Finance real-time quote page](https://finance.sina.com.cn/realstock/company/{exchange}{stock_code}/nc.shtml)
- [Tencent Finance quote page](https://gu.qq.com/{exchange}{stock_code})
- [10jqka stock page](https://stockpage.10jqka.com.cn/{stock_code}/)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Chinese-language analysis text plus an HTML report template suitable for browser rendering and PDF export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public finance data sources and includes report sections for core view, price structure, data analysis, scenarios, risk factors, and summary.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
