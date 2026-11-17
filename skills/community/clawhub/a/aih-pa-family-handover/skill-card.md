## Description:

根据家庭成员自愿提供的空闲时段、接送事件和责任规则，生成家庭分工表、接送日历和交接卡，并标记尚未确认的安排。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

家庭成员和协助安排日程的人可将自愿提供的时间、活动和责任规则整理成可审阅的分工表、接送日历及交接卡，识别无人确认的接送任务。共享日历或发送消息需要另行授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A suggested pickup assignment may be mistaken for a confirmed commitment.

Mitigation: Keep suggestions separate from acceptance and flag any unconfirmed pickup for review.

Risk: Sharing family schedules could disclose a child's location.

Mitigation: Share location only with confirmed pickup participants when necessary and obtain authorization before sharing calendars or messages.

Risk: Optional AI-HIVE use could upload sensitive family details or incur charges.

Mitigation: Confirm the permitted data scope, current price, currency, and spending limit before uploading or paying; do not provide passwords, tokens, or verification codes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-family-handover)
- [家庭分工与接送执行流程](references/workflow-12.md)
- [结果与证据要求](references/output-contract.md)
- [AI-HIVE 接入与授权说明](references/ai-hive-connection.md)
- [产品范围与来源](references/scope-and-sources.md)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [CSV family assignments, iCalendar (.ics) pickup schedule, and text handover cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; unconfirmed assignments remain explicitly unconfirmed. Sharing requires separate authorization.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
