## Description:

Amemo Skill connects AI agents to Amemo cloud services for managing notes, tasks, health data, and assistant memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lockfeel](https://clawhub.ai/user/lockfeel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use the skill to log in to Amemo, save and search notes, manage task reminders, retrieve health summaries, and synchronize assistant memory with Amemo cloud services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login tokens and personal data may be stored in skill files.

Mitigation: Use the skill only in trusted personal workspaces and remove tokens or personal data before sharing the workspace.

Risk: Notes, tasks, health data, email addresses, and assistant memory may be sent to Amemo cloud services.

Mitigation: Install only when comfortable with Amemo receiving that data, and avoid sending sensitive work or regulated information.

Risk: Assistant memory synchronization may include broad memory content without preview or redaction.

Mitigation: Review and redact memory content before synchronization, and avoid storing secrets in memory files.

## Reference(s):

- [Health Summary Templates](modules/amemo-last-data/references/health-templates.md)
- [Amemo Skill on ClawHub](https://clawhub.ai/lockfeel/skills/amemo-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with JSON API payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local skill configuration and memory files during login and memory synchronization flows.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
