## Description: <br>
Generates AI-enhanced DTC business analysis reports from local management, business, and budget spreadsheets, covering budget-versus-actual performance, trends, customer and sales views, overseas warehouse analysis, key findings, and HTML report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangliangliang909-oss](https://clawhub.ai/user/zhangliangliang909-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, finance operators, and agent users use this skill to generate monthly, quarterly, or annual DTC operating reports from local DTC spreadsheet workspaces and review budget attainment, revenue, profit, customer, sales, and warehouse trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local DTC business-data workspaces that may contain sensitive customer names, sales rankings, revenue, profit, and loss-customer details. <br>
Mitigation: Run it only against the intended workspace, verify source paths before execution, and restrict access to generated reports. <br>
Risk: Generated financial and operating calculations may be misleading if source data, report period, or business rules are wrong. <br>
Mitigation: Validate data freshness, calculation rules, and generated totals before using the report for business decisions. <br>
Risk: Generated HTML reports may load Chart.js from a remote CDN. <br>
Mitigation: Remove, pin, or vendor the Chart.js dependency before opening reports in sensitive environments or sharing externally. <br>
Risk: Reports can expose customer, sales, revenue, profit, and loss-customer details when shared. <br>
Mitigation: Review and redact generated HTML, Markdown, or Excel outputs before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangliangliang909-oss/dtc-report) <br>
- [DTC Report AI analysis guide](artifact/AI_ANALYSIS_GUIDE.md) <br>
- [DTC report data rules](artifact/references/data_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [HTML reports, Markdown summaries, Excel files, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local DTC business-data workspace and can produce reports containing financial, customer, sales, and warehouse details.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata and SKILL.md changelog, released 2026-04-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
