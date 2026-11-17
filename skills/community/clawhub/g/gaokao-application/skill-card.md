## Description:

用于帮助大陆高考学生或家长选择大学、专业、院校专业组，或制定志愿填报策略。支持省份规则、位次匹配、用户上传录取数据，以及谨慎的冲稳保垫规划。不会保证录取。

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially mainland China Gaokao students and parents, use this skill to prepare cautious college application plans from province rules, rank, subject choices, admission data, preferences, and risk tolerance.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Generated application plans can be wrong or outdated if current province rules, enrollment plans, codes, tuition, campus details, or restrictions have changed.

Mitigation: Verify final choices against current official sources such as the provincial examination authority, university admissions documents, and Sunshine Gaokao before submission.

Risk: Untrusted CSV admission data can mislead recommendations or create spreadsheet risk when opened outside the agent workflow.

Mitigation: Prefer official data, validate CSV columns before use, and avoid opening generated CSVs in spreadsheets unless the source is trusted or formula-prefixed cells are neutralized.

Risk: Historical rank matching is decision support, not an admission guarantee.

Mitigation: Present rank bands and shortlist results with cautious language, explain uncertainty, and avoid guaranteed-admission claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/gaokao-application)
- [Workflow](references/workflow.md)
- [Data Contract](references/data-contract.md)
- [Province Rule Checklist](references/province-rules.md)
- [Risk Policy](references/risk-policy.md)
- [Output Templates](references/output-templates.md)
- [Source Checklist](references/source-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown guidance with optional CSV files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask intake questions before making recommendations; optional helpers produce local CSV outputs from user-provided admissions data.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
