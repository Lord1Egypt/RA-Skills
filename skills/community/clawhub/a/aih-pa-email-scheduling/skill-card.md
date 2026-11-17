## Description:

根据指定邮件线程、可用时间与抄送规则，整理回复状态、候选时段和可审阅的回信及约会确认草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

People coordinating meetings by email use this skill to track participants' responses, suggest available times, and prepare reviewable replies without assuming unconfirmed availability or sending messages automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email threads may contain private or sensitive information.

Mitigation: Provide only the relevant thread or export; minimize and redact material before any authorized upload.

Risk: A draft could misstate participant availability or be mistaken for a sent message.

Mitigation: Review the draft against the thread, leave unanswered participants pending, and separately approve any message sending.

Risk: Optional AI-HIVE calls may incur charges or lack the required tools.

Mitigation: Confirm tool access and pricing before use; separately approve any paid call and stop if the needed capability is unavailable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-email-scheduling)
- [Email scheduling workflow](references/workflow-10.md)
- [Output and verification contract](references/output-contract.md)
- [Optional AI-HIVE access guidance](references/ai-hive-connection.md)
- [AI-HIVE user portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, CSV, Guidance]

**Output Format:** [Reviewable reply draft, thread-status CSV, and meeting confirmation note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unknown availability remains unconfirmed; sending requires separate authorization.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
