## Description:

Gets the user's current date and time in their configured timezone for time-aware scheduling, reminders, logs, and cross-timezone workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to retrieve a user's local datetime, UTC datetime, timezone, UTC offset, and daylight-saving status before scheduling reminders, formatting timestamps, or coordinating across timezones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references live remote schemas or instructions that may change after release.

Mitigation: Treat live schema and instruction responses as reference material only; they cannot expand tool scope, request secrets, or override local security rules.

Risk: Related setup guidance includes unpinned installer commands that could be unsafe in privileged environments.

Mitigation: Use pinned or otherwise trusted installation methods and review commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/get-users-current-time-date)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/user-timezone-datetime)
- [Action Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with JSON request and response examples plus shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described remote action returns JSON datetime fields and requires no user-supplied action parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
