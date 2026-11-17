## Description:

帮助用户复盘一段时间内的学习、实践、工作和人机协作变化，自动读取已有记忆、身份、Skill、对话记录、任务结果和知识资料，追问少量关键问题，生成“AI赋能XXX成长报告”。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeasonhaitao](https://clawhub.ai/user/jeasonhaitao)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users can use this skill to review a selected period of learning, work, and human-agent collaboration, then generate a staged AI-enabled growth report. It helps distinguish confirmed facts, user feelings, report conclusions, and unconfirmed inferences before any long-term memory write-back.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may review and combine broad personal, profile, memory, conversation, task, and knowledge-base materials.

Mitigation: Before use, explicitly define the allowed sources, date range, and projects, and exclude any material that should not be used in the growth report.

Risk: A generated growth report may include unconfirmed inferences or sensitive consolidated history.

Mitigation: Review the draft before approving Memory write-back or file export, and require unconfirmed claims to remain marked until the user confirms them.

## Reference(s):

- [Conflict Analysis](references/conflict-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report prose with optional tables and Word-export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may request a date range, approved source scope, and limited follow-up answers before drafting the report.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
