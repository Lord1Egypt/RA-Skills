## Description:

将商家联系方式、可约时间、服务要求和沟通授权整理成预约电话简报、通话结果记录及预约核对表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

需要安排服务预约的用户可用它准备电话询问要点和备选时段，并记录实际答复、费用及取消条款。没有获授权的电话服务时，只生成可供人工拨打和核对的材料。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone calls, uploads or paid AI-HIVE tasks may exceed the user's intended authorization or budget.

Mitigation: Confirm the service, data scope, current price, budget and explicit authorization before taking external action; otherwise provide a draft for review.

Risk: Sensitive credentials or identity data could be exposed through chat or uploads.

Mitigation: Do not request passwords, verification codes, tokens, cookies or full identity documents in chat; minimize and de-identify any uploaded materials.

Risk: An unmade call or unverified reply could be mistaken for a confirmed booking.

Mitigation: Record only actual replies as confirmations and clearly mark missing phone tools, unknown details and uncompleted bookings.

## Reference(s):

- [预约电话执行与验收流程](references/workflow-05.md)
- [结果与证据核对说明](references/output-contract.md)
- [AI-HIVE 登录与授权说明](references/ai-hive-connection.md)
- [AI-HIVE 网页入口](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Plain text appointment brief and checklist; call record in text or optional JSON/CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; distinguish confirmed responses from unknown or unexecuted actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
