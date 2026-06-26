## Description: <br>
Data Analysis Init helps PMO agents set up long-running business data analysis plans that combine Feishu or CSV/Excel data, schema parsing, search enrichment, and standardized reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winsaney](https://clawhub.ai/user/winsaney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
PMO agents and business teams use this skill to initialize recurring KPI reviews, competitor price monitoring, traffic attribution analysis, and other data-backed business monitoring workflows. It guides agents through goal alignment, data schema setup, report template design, search strategy configuration, trial runs, and ongoing monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive business metrics, customer data, internal identifiers, or confidential incidents could be exposed through web-search queries or shared reports. <br>
Mitigation: Keep sensitive details out of search queries and review generated reports, search strategies, and schema configs before sharing them. <br>
Risk: Spreadsheet schema inference and external attribution can produce misleading conclusions when data is incomplete, inconsistent, or poorly defined. <br>
Mitigation: Confirm field meanings, metric formulas, data access, and flagged data anomalies before using generated reports for decisions. <br>


## Reference(s): <br>
- [Analysis report template](assets/analysis-report-template.md) <br>
- [Schema format example](references/schema-format-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and generated report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates runtime files under ./user-data/ for schema configuration, search strategy, and analysis reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
