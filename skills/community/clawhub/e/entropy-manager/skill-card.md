## Description:

熵管理系统用于管理和控制AI会话中的熵，包括上下文精简、状态重置、注意力聚焦和熵预警，适用于长时间会话、复杂任务和多步骤工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to assess conversation drift, summarize overgrown context, reset task state, and focus the next action during long or complex sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context pruning or state resets may remove useful details from a long conversation.

Mitigation: Preview summaries and state resets before relying on them, and confirm important decisions, constraints, and next actions are retained.

Risk: Entropy levels and focus recommendations are heuristic and may misread the current task state.

Mitigation: Treat the report as guidance and compare it with the user's current goal before narrowing or changing the conversation state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/entropy-manager)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, summaries, state cards, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, file access, network calls, credential use, or persistent changes indicated by security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
