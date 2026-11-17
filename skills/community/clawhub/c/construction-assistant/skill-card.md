## Description:

施工项目管理助手。支持施工进度跟踪、材料清单管理、安全检查记录、施工日志生成、工程量计算。使用场景：(1) 创建/更新施工进度计划，(2) 管理材料和设备清单，(3) 记录安全检查和整改，(4) 生成施工日志和报告，(5) 计算工程量和成本估算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuawang658-gif](https://clawhub.ai/user/jinhuawang658-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Construction project staff and external project teams use this skill to create and update schedules, track work progress, estimate materials, record safety checks, generate daily or weekly reports, and calculate common quantities for construction management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local schedules and reports can be created or updated, and evidence.security notes overwrite-related bugs.

Mitigation: Use version control or backups before running the file-based scripts and review output paths before execution.

Risk: Generated dates, progress records, safety checks, and compliance records may be inaccurate.

Mitigation: Have qualified project staff manually verify dates, progress status, quantities, and safety or compliance records before relying on them.

Risk: Material reporting behavior can create paired report files and evidence.security advises choosing Markdown output names.

Mitigation: Use explicit .md output paths for material reports and inspect generated companion files before sharing or archiving them.

## Reference(s):

- [Construction report templates](references/report_templates.md)
- [Safety inspection checklist](references/safety_checklist.md)
- [Quantity calculation formulas](references/quantity_formulas.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local schedule, progress, report, material, quantity, and safety record files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
