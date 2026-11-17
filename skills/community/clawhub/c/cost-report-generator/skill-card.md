## Description:

Generates formatted Excel cost analysis reports from project expense workbooks, grouping customer categories such as 帝国, BAT, MT, and ITMS and summarizing 2025 and 2026 costs by month and year.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard052317](https://clawhub.ai/user/richard052317)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, operations, and project teams use this skill to turn customer project expense workbooks into categorized annual, monthly, and average cost reports. It is intended for user-directed report generation from trusted or reviewed Excel inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel reports may preserve formula-like text from source workbooks as active spreadsheet content.

Mitigation: Review the skill before using customer, vendor, or otherwise untrusted files; sanitize spreadsheet text or use only trusted input workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard052317/skills/cost-report-generator)
- [Skill instructions](artifact/SKILL.md)
- [Cost report generation script](artifact/scripts/generate_cost_report.py)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Code]

**Output Format:** [Excel workbook (.xlsx) with brief command-line status text and Python invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workbook contains formatted 2025 and 2026 cost-analysis worksheets with grouped customer categories and monthly cost summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
