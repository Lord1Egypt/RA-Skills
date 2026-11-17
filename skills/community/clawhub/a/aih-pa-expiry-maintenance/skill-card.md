## Description:

将证件与保养事项的到期日期、适用对象、官方来源和提醒窗口整理为到期台账、准备清单及日历提醒草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人与家庭用户可整理证件续期、车辆保养等到期事项，生成可核对的提醒和办理准备材料；办理提前量和所需材料须以适用的官方规则核验。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive identity data or credentials could be disclosed when preparing or uploading materials.

Mitigation: Do not request full ID numbers or credentials in chat; minimize or redact materials and confirm upload scope before external use.

Risk: Optional AI-HIVE access may involve external authorization, uploads, or paid model calls.

Mitigation: Keep local drafting as the default; confirm actual tools, prices, currency, budget, and upload scope before use.

Risk: Incorrect renewal rules or assumed travel eligibility could lead to misleading reminders.

Mitigation: Check applicable official rules and sources, mark missing facts for review, and do not promise successful processing or travel eligibility.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-expiry-maintenance)
- [任务流程与验收](references/workflow-49.md)
- [AI-HIVE 接入说明](references/ai-hive-connection.md)
- [AI-HIVE 网页入口](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [CSV expiry ledger, preparation checklist, and iCalendar (.ics) file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; unknown facts remain marked as unknown, with source references for task fields.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
