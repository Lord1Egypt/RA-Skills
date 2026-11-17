## Description:

成本分配表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

制造企业的成本会计可在月度成本结账和产成品入库前使用该技能，核对成本分配表的合计行、投入合计、成本守恒、重复行、空白项和负成本等问题。它适用于对已导出或粘贴的文本表格做本地检查，不替代会计判断、审计程序或税务判断。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks arithmetic and table consistency but may be mistaken for accounting, audit, or tax advice.

Mitigation: Use findings as local review aids only, and have qualified accounting, audit, or tax personnel make final judgments.

Risk: The checker does not inspect ERP, MES, financial systems, source vouchers, or record authenticity directly.

Mitigation: Export or paste the relevant table text yourself and reconcile any flagged issue against the source systems and supporting records.

Risk: The free edition intentionally omits some advanced checks such as method validation, unit-cost outlier detection, and zero ending-WIP-cost detection.

Mitigation: Review the listed withheld checks before relying on a clean result, especially for close, audit, or tax-support workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cost-allocation-check-free)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON report with cited findings and local Node.js command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on provided cost-allocation table text; JSON output is available with --json.]

## Skill Version(s):

1.0.20 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
