## Description:

分析猫适口性双盆试验 Excel 数据，清洗异常记录，并生成统计汇总、Markdown 报告和图表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongmuh](https://clawhub.ai/user/dongmuh)

### License/Terms of Use:

MIT

## Use Case:

宠物食品研发与适口性试验人员可使用此技能分析符合指定模板的猫双盆试验 Excel 记录，检查异常数据，并查看 A/B 采食比较、首选率、配对显著性及采食量统计。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan covered 14 of 16 components, so its benign verdict has medium confidence and does not cover every component.

Mitigation: Review the skill and its Python dependencies before installation; treat the scan verdict as limited to the components it examined.

Risk: The analyzer expects a specific workbook sheet and column layout, so a different template can cause errors or misleading results.

Mitigation: Confirm the workbook matches the documented format and review the generated report and removed-record list before using the analysis.

## Reference(s):

- [统计口径详细说明](references/statistical_rules.md)
- [ClawHub 发布页](https://clawhub.ai/dongmuh/skills/cat-palatability-analysis)

## Skill Output:

**Output Type(s):** [Analysis, CSV files, Excel workbook, Markdown report, Charts]

**Output Format:** [CSV, XLSX, Markdown, and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cleaned and removed records, group and meal summaries, paired-test results, preference metrics, and visualizations.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
