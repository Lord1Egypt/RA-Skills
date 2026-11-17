## Description:

(半自动) 投放素材效果诊断与分析，通过读取平台导出的数据报表（图片或表格），生成一份诊断分析报告，为素材优化提供明确建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, growth teams, and agents use this skill to analyze exported advertising creative CSV reports, rank strong and weak creatives, classify performance patterns, and produce optimization guidance for future material iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown may contain misleading analysis or untrusted campaign data from user-provided CSV files.

Mitigation: Review generated reports before using, sharing, or asking another AI to expand them.

Risk: Advertising reports may include campaign names or other sensitive business data.

Mitigation: Use only report files the user intentionally selects and avoid sharing outputs through external channels unless the data is approved for that audience.

Risk: CSV values may be interpreted as instructions by a downstream AI.

Mitigation: Treat campaign names and other CSV-derived values as report data, not executable or authoritative instructions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic report with tables, rankings, quadrant classification, keyword insights, and optimization recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-selected CSV reports and column mappings; output should be reviewed before sharing or expanding with another AI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
