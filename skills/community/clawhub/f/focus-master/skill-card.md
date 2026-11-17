## Description:

Focus Master helps agents guide users through Pomodoro timers, task time tracking, productivity analytics, focus mode, and efficiency reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage focused work sessions, track task history, review time allocation, and generate productivity reports from a local CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local task history and configuration data under ~/.openclaw/data/time-management/.

Mitigation: Review local data retention expectations and remove or protect stored task history when it may contain sensitive work details.

Risk: The inspected artifact did not include the time-management executable referenced by the skill.

Mitigation: Verify the executable supplied by the publisher before installation or use.

## Reference(s):

- [Focus Master on ClawHub](https://clawhub.ai/harrylabsj/skills/focus-master)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local task history and configuration files under ~/.openclaw/data/time-management/.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
