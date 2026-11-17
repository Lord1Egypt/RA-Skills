## Description:

每日Get笔记智能盘点 - 扫描+分类+自动处理+CRM更新

This skill is ready for commercial/non-commercial use.

## Publisher:

[skychentian](https://clawhub.ai/user/skychentian)

### License/Terms of Use:


## Use Case:

Users who keep daily Get note recordings use this skill to scan the last 24 hours of local recordings, classify business-relevant items, and produce follow-up reports or CRM and task updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private local recordings and write derived business data into external CRM and task systems.

Mitigation: Install only when those reads and writes are expected, require explicit review before external writes, and configure approved destinations narrowly.

Risk: Scheduled daily or midnight runs could process sensitive recordings without timely human oversight.

Mitigation: Avoid enabling scheduled runs until redaction, audit logging, rollback, and approval controls are in place.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report with categorized summaries, CRM update details, task lists, and priority reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update Feishu CRM records and TickTick task lists when those destinations are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
