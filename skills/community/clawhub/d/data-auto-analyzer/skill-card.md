## Description: <br>
数据自动分析 helps agents analyze Excel and CSV files, diagnose advertising account performance, evaluate A/B tests, and generate daily performance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ming0429](https://clawhub.ai/user/ming0429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, data analysts, and business teams use this skill to turn local spreadsheet exports into interactive reports, account diagnostics, A/B test conclusions, and daily summaries. It is especially suited to advertising performance data, but can also process general structured business tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded or explicitly referenced spreadsheets may contain sensitive business data. <br>
Mitigation: Use the skill only for files the user intends to analyze, and keep generated reports in the local output directory unless the user asks to share them. <br>
Risk: Generated HTML reports may contact cdnjs to load ECharts when opened. <br>
Mitigation: Use an offline ECharts bundle or review the generated HTML before opening it in restricted environments. <br>
Risk: Broad prompts can trigger spreadsheet analysis when files are present. <br>
Mitigation: Confirm the target file and intended mode when the user's request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ming0429/data-auto-analyzer) <br>
- [A/B Test Guide](references/ab_test_guide.md) <br>
- [Daily Report Format](references/daily_report_format.md) <br>
- [Diagnosis Rules](references/diagnose_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands; generated local HTML and TXT reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports are written locally, normally under data-auto-analyzer/; HTML reports may load ECharts from cdnjs when opened.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
