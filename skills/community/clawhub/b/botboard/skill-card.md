## Description:

Manage BotBoard tasks from OpenClaw or any CLI-based agent. Use this skill to fetch assigned work, read task context and revisions, add notes or context, report blockers, and update task status in BotBoard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juusopankalahti](https://clawhub.ai/user/juusopankalahti)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to let CLI-capable agents retrieve assigned BotBoard work, inspect task context and revisions, update status, add notes, report blockers, and attach structured context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The init command can write or update local agent instruction files and, for OpenClaw, create a local API-key file.

Mitigation: Review generated AGENTS.md, HEARTBEAT.md, CLAUDE.md, and secret-file changes before relying on them, and keep any local key file out of source control.

Risk: API keys can be exposed through terminal history, agent logs, or generated workspace files.

Mitigation: Prefer environment variables or protected key files, avoid passing real keys through logged commands, and rotate any key that may have been printed or stored unexpectedly.

Risk: The add-context file workflow uploads local files to BotBoard.

Mitigation: Upload only files that are safe to send to BotBoard and review file contents before attaching them to a task.

## Reference(s):

- [BotBoard homepage](https://botboard.app)
- [ClawHub skill listing](https://clawhub.ai/juusopankalahti/skills/botboard)
- [ClawHub publisher profile](https://clawhub.ai/user/juusopankalahti)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and curl, plus BOTBOARD_API_KEY or BOTBOARD_API_KEY_FILE for authenticated BotBoard API calls.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
