## Description:

数据自动分析 is a local spreadsheet analysis and advertising optimization skill for Excel or CSV reports, covering general analysis, account diagnosis, A/B test analysis, and daily report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ming0429](https://clawhub.ai/user/ming0429)

### License/Terms of Use:

MIT-0

## Use Case:

External users, advertising optimizers, operations teams, and data analysts use this skill to analyze structured spreadsheet data, diagnose campaign performance, compare A/B test results, and generate daily advertising reports. It supports common ad-platform exports as well as general sales, finance, and operations tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute script derived from spreadsheet content.

Mitigation: Run the skill only on trusted spreadsheets, review generated reports before sharing, and fix HTML escaping before broader deployment.

Risk: Generated HTML reports load ECharts from a third-party CDN.

Mitigation: Use a local bundled ECharts copy and pinned dependencies when handling sensitive business data or offline workflows.

Risk: The security verdict is suspicious for this release.

Mitigation: Treat installation and report output as requiring review until the identified HTML escaping and script-loading issues are resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ming0429/skills/data-auto-analyzer)
- [Metadata homepage](https://clawhub.ai/ming0429/data-auto-analyzer)
- [A/B test guide](references/ab_test_guide.md)
- [Daily report format](references/daily_report_format.md)
- [Diagnosis rules](references/diagnose_rules.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands; generated reports are HTML and plain text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files default to the data-auto-analyzer/ directory and can be redirected with DATA_AUTO_ANALYZER_OUTDIR or output flags.]

## Skill Version(s):

4.0.1 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
