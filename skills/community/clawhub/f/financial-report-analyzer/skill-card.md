## Description: <br>
Financial Report Analyzer extracts financial metrics from uploaded PDF financial reports and produces charts and Markdown analysis for Chinese A-share, Hong Kong, and US-listed companies. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[hj2916](https://clawhub.ai/user/hj2916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, investors, students, and finance teams use this skill to locally extract metrics from PDF financial reports, compare company financial health, and generate reference analysis reports with charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON, text, chart, and report files can persist financial information from user-provided PDFs on the local filesystem. <br>
Mitigation: Run the skill in a dedicated folder, avoid confidential non-public reports unless local plaintext outputs are acceptable, and delete generated artifacts when finished. <br>
Risk: The generated report may include overconfident investment-style ratings, recommendations, or conclusions. <br>
Mitigation: Treat all investment language as non-professional reference analysis and independently verify it before making decisions. <br>
Risk: Automated PDF extraction can misread tables or miss key metrics, especially when report formats vary. <br>
Mitigation: Review extracted values against the source PDF and manually check important calculations before relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hj2916/financial-report-analyzer) <br>
- [Financial metrics reference](references/financial_metrics.md) <br>
- [Financial analysis report template](references/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown analysis reports, local chart image files, extracted text or JSON data, and inline shell commands for local Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated locally from user-provided PDFs and may include plaintext financial data, chart images, and non-professional investment-style commentary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG, released 2026-03-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
