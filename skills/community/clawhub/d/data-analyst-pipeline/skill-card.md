## Description: <br>
数据分析师skill automates a local data analysis workflow for loading CSV, Excel, JSON, and SQLite datasets, auditing data quality, cleaning data, running EDA, creating visualizations, and generating an interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to run a repeatable local data-analysis pipeline over tabular datasets and produce quality checks, summaries, charts, and an HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected datasets and generated reports, charts, summary JSON, and terminal output may contain sensitive data. <br>
Mitigation: Run it only on datasets you are authorized to analyze, write outputs to approved locations, and review reports before sharing. <br>
Risk: Report text and HTML content are built from dataset-derived names and values, so untrusted datasets can influence generated output. <br>
Mitigation: Avoid untrusted datasets or sanitize and review dataset names, columns, and values before opening or distributing generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/data-analyst-pipeline) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Business rules configuration](config/business_rules.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and Python snippets; generated artifacts include HTML reports, PNG charts, JSON summaries, and terminal output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports and summaries may include dataset-derived names, values, statistics, and charts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
