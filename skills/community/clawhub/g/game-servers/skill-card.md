## Description:

Order, configure and manage dedicated game servers (20+ games) via Supercraft REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcjkrs](https://clawhub.ai/user/mcjkrs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to order, configure, and operate Supercraft dedicated game servers through the Supercraft REST API, including catalog browsing, purchases, server lifecycle actions, configuration, logs, connection details, and console commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The login flow may create a recurring cron-based polling task without clear cleanup or explicit user consent.

Mitigation: Avoid persistent cron polling unless the user explicitly approves a bounded, removable task; prefer polling during the active session or after the user's next message.

Risk: JWTs and magic-link tokens could be exposed through command lines, logs, or scheduler entries.

Mitigation: Keep tokens out of command arguments, logs, and scheduler definitions; store credentials only in secure session-local mechanisms when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mcjkrs/skills/game-servers)
- [Supercraft API Homepage](https://claws.supercraft.host)
- [Getting Started Guide](https://claws.supercraft.host/documentation-for-agents/getting-started.md)
- [OpenAPI Reference](https://claws.supercraft.host/docs)
- [Machine-readable Discovery](https://supercraft.host/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with REST API endpoints and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated API request guidance for Supercraft server management workflows.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
