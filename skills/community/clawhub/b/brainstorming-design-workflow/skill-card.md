## Description:

Guides agents through collaborative design brainstorming before creative implementation work by clarifying intent, constraints, success criteria, and implementation approach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to turn early feature or behavior-change ideas into validated design specs before implementation. It supports collaborative requirement discovery, option comparison, incremental design review, and follow-on planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation language may trigger the workflow for many creative coding tasks.

Mitigation: Confirm that design brainstorming is appropriate for the current task before applying the workflow.

Risk: The workflow asks the agent to inspect repository context and recent commits.

Mitigation: Limit repository inspection to task-relevant files and avoid exposing sensitive project details in shared outputs.

Risk: The workflow may ask the agent to write and commit a design document.

Mitigation: Keep file writes and git commits explicitly user-approved and review generated design documentation before committing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhengxinjipai/skills/brainstorming-design-workflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational guidance and Markdown design documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include step-by-step questions, design sections, trade-off analysis, documentation updates, and suggested follow-on implementation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
