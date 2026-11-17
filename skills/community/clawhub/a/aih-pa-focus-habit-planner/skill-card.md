## Description:

根据可用时间、任务规模、优先级和休息要求生成可核对的周排程、习惯清单及时间冲突说明。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人和团队可用此助手把待办任务与习惯安排进实际可用时段，生成可审阅的每周计划，并识别容量不足和日程冲突。可选用 AI-HIVE 辅助处理，但外部操作取决于实际工具与用户授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private scheduling information or credentials could be exposed when using optional AI-HIVE tools.

Mitigation: Keep passwords, tokens, and verification codes out of chats; minimize and review the data scope before any upload.

Risk: Optional paid calls or external calendar changes could incur costs or alter user data.

Mitigation: Confirm available tools, price, currency, spending limit, and explicit authorization before paid or external actions.

Risk: An overfilled plan could misrepresent what fits in the available time or sacrifice rest.

Mitigation: Show trade-offs or defer tasks when capacity is insufficient, and preserve fixed commitments and rest blocks.

## Reference(s):

- [ClawHub 技能发布页](https://clawhub.ai/wubin1836/skills/aih-pa-focus-habit-planner)
- [排程流程与验收规则](references/workflow-15.md)
- [结果与证据说明](references/output-contract.md)
- [AI-HIVE 接入与授权说明](references/ai-hive-connection.md)
- [AI-HIVE 官方入口](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [CSV weekly schedule with a habit checklist and conflict notes in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; preserve fixed commitments and rest periods, and identify unresolved inputs or unperformed external actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
