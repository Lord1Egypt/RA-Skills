## Description:

Your personal AI assistant platform for multi-agent orchestration, task management, and autonomous workflow execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyanhui](https://clawhub.ai/user/shiyanhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to connect an agent to the 1Person assistant service for multi-agent task orchestration, workflow execution, persistent memory, and task management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external assistant service and requires ONEPERSON_API_KEY.

Mitigation: Protect ONEPERSON_API_KEY like a password and rotate or revoke it if it is exposed.

Risk: Sensitive work sent to the external 1Person service may be handled outside the local agent environment.

Mitigation: Review 1Person's policies before sending sensitive data or regulated work through the skill.

Risk: Persistent memory may retain task context across sessions.

Mitigation: Confirm how stored memory can be reviewed or deleted before using the skill for sensitive workflows.

## Reference(s):

- [1Person homepage](https://1person.pro)
- [1Person documentation](https://docs.1person.pro)
- [ClawHub skill page](https://clawhub.ai/shiyanhui/skills/1person)
- [Publisher profile](https://clawhub.ai/user/shiyanhui)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with environment variable setup instructions and service-directed task output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ONEPERSON_API_KEY and use of the external 1Person service.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
