## Description: <br>
Generates Chinese A-share stock strategy research reports in HTML/PDF-ready form from public market, financial, capital-flow, industry, and disclosure data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill-lib](https://clawhub.ai/user/bill-lib) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn an A-share stock code or company name into a structured Chinese strategy research report covering price structure, fundamentals, scenarios, risks, and summary judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial figures or market data may be stale, unavailable, or inconsistent across public data sources. <br>
Mitigation: Verify prices, fundamentals, and event data against authoritative finance sources before relying on the report. <br>
Risk: Generated strategy commentary could be mistaken for investment advice. <br>
Mitigation: Treat the report as analytical assistance only and require human financial judgment before any trading or investment decision. <br>
Risk: The skill may trigger on simple stock-code mentions and perform multiple external finance-site lookups. <br>
Mitigation: Confirm user intent for stock research workflows and monitor external lookups in environments with network or compliance constraints. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bill-lib/a-stock-analysis-lite) <br>
- [Publisher profile](https://clawhub.ai/user/bill-lib) <br>
- [README](README.md) <br>
- [Data sources and collection rules](references/data-sources.md) <br>
- [Analysis prompts](references/analysis-prompts.md) <br>
- [HTML report template and quality checklist](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Chinese Markdown analysis with HTML report output that can be printed or saved as PDF] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public finance-site lookups and a fixed report structure with quality checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
