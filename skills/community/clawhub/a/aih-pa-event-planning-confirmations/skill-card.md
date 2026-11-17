## Description:

将活动人数、地点、预算、时间和参与者回复整理成筹备看板、确认名单与活动日程，并在获得授权且工具可用时协助后续执行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

活动组织者和个人助理可用此技能根据参与者明确回复编制筹备看板、确认名单、日程及场地或票务核对清单；对外通知和购票须另行授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Participant details or other sensitive materials may be disclosed through optional uploads.

Mitigation: Confirm the AI-HIVE domain and upload scope; minimize and redact data before transfer.

Risk: Messages, ticket purchases or other external changes may occur without informed consent or exceed budget.

Mitigation: Obtain separate explicit authorization for each external action and confirm current prices, currency and a spending limit.

Risk: Tentative participants or unavailable tools could be mistaken for confirmed attendance or completed bookings.

Mitigation: Count only explicit confirmations, verify available tools and receipts, and label unexecuted work as a draft.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-event-planning-confirmations)
- [活动筹备执行与验收流程](artifact/references/workflow-57.md)
- [结果与证据合同](artifact/references/output-contract.md)
- [AI-HIVE 连接与授权说明](artifact/references/ai-hive-connection.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Markdown; optional CSV or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviewable planning board, confirmation list and schedule; unknown details remain marked as unknown.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
