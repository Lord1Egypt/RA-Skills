## Description:

A Chinese-language motivation and task-progress management skill that helps agents generate positive encouragement, track tasks, celebrate milestones, enter focus mode, and summarize completed work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate positive Chinese-language encouragement, manage task progress, record milestones, and review completion status during work sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The task tracker stores task names, milestones, progress, and timestamps locally at ~/.openclaw/agent-motivator/task_state.json.

Mitigation: Avoid entering sensitive task details unless local storage in that path is acceptable.

## Reference(s):

- [Positive Motivation Principles](references/motivation_principles.md)
- [ClawHub Skill Page](https://clawhub.ai/linux2010/skills/agent-motivator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Chinese-language motivational text and local task-tracking records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
