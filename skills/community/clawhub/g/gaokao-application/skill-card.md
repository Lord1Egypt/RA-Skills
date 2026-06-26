## Description: <br>
用于帮助大陆高考学生或家长选择大学、专业、院校专业组，或制定志愿填报策略。支持省份规则、位次匹配、用户上传录取数据，以及谨慎的冲稳保垫规划。不会保证录取。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, parents, and education advisors use this skill to build cautious mainland China Gaokao application plans from province rules, rank, selected subjects, preferences, and official or user-provided admission data. It produces risk-labeled shortlists, ordering guidance, and final verification checklists without guaranteeing admission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Application advice may be mistaken for an admissions guarantee. <br>
Mitigation: State that the skill is decision support only, avoid guaranteed-admission language, and require users to verify final choices against current official sources. <br>
Risk: Outdated or unofficial admission data can lead to incorrect shortlists or ordering. <br>
Mitigation: Use official provincial examination authority, university admissions, and Sunshine Gaokao sources for current rules, codes, plans, restrictions, tuition, and source dates. <br>
Risk: Province-specific rules, selected-subject requirements, or special-category restrictions may materially change eligibility. <br>
Mitigation: Confirm province, year, batch, subject track, filing model, special category, physical examination, language, single-subject, gender, political review, and transfer-adjustment restrictions before recommending a final plan. <br>
Risk: CSV helper outputs may contain normalization or data-quality errors. <br>
Mitigation: Validate required columns, preserve official codes as strings, flag missing ranks or source fields, and review generated CSV outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/gaokao-application) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Workflow](artifact/references/workflow.md) <br>
- [Data Contract](artifact/references/data-contract.md) <br>
- [Province Rule Checklist](artifact/references/province-rules.md) <br>
- [Risk Policy](artifact/references/risk-policy.md) <br>
- [Output Templates](artifact/references/output-templates.md) <br>
- [Source Checklist](artifact/references/source-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, CSV-oriented helper commands, and optional generated CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should use Chinese by default, rely on rank as the primary matching signal, label risk bands, and include official-source verification before final submission.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
