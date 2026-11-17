## Description:

广告投放数据分析。当用户上传 Excel/CSV 广告报表，或说"帮我分析投放数据/看看这个报表/哪个计划效果差/数据有没有问题"时触发。自动识别所有表头列，无需预设字段名，汇总全部指标，检测异常，生成可视化图表，输出分析报告和优化建议。支持巨量引擎、腾讯广告、Meta Ads、Google Ads、快手等平台导出格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ming0429](https://clawhub.ai/user/ming0429)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, analysts, and agent users can use this skill to analyze user-provided advertising Excel or CSV reports, identify metrics and anomalies, generate local charts, and draft optimization guidance across common ad-platform export formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertising reports can contain sensitive business data.

Mitigation: Run the analyzer only on reports intentionally provided by the user and keep generated chart files in an appropriate local output folder.

Risk: Automated optimization suggestions may be incomplete or misleading for business decisions.

Mitigation: Review the generated recommendations against campaign context before changing budgets, pausing ads, or reallocating spend.

Risk: The skill installs standard Python data-analysis packages and writes PNG outputs.

Mitigation: Use a trusted Python environment and choose an output directory where generated chart files are expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ming0429/skills/ad-analyzer-yima)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples, console analysis text, and local PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus pandas, openpyxl, xlrd, matplotlib, and seaborn; reads user-provided Excel/CSV files locally and writes charts to the selected output directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
