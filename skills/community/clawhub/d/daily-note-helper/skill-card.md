## Description:

整理零散日常记录、会议随手记、工作流水和个人复盘内容，输出清晰的每日摘要、待办事项、风险提醒和明日计划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingyuzhang-alt](https://clawhub.ai/user/jingyuzhang-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to turn rough daily notes, meeting fragments, work logs, or personal reflections into concise daily summaries, todos, risks, and next-day suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit activation may cause the agent to organize rough daily notes automatically when the user provides note-like fragments.

Mitigation: Review sensitive meeting notes or personal reflections before sharing them with an agent, and confirm the generated summary before relying on it.

Risk: Ambiguous notes can be rewritten into action-oriented bullets that may still need clarification.

Mitigation: Keep uncertain details marked as `待确认` and avoid adding names, deadlines, metrics, or decisions that are not present in the source notes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily-note summary with sections for overview, completed items, todos, risks or blockers, and next-day suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to concise Chinese unless the source material or user request calls for another language or format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
