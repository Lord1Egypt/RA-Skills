## Description:

Create a living agent from your Discord server. The agent embodies your community's identity, remembers every conversation, and grows as the community evolves. Talk to your Discord as if it were a person.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgeesawor](https://clawhub.ai/user/kgeesawor)

### License/Terms of Use:

MIT

## Use Case:

Developers and community operators use Discord Soul to turn authorized Discord server exports into an OpenClaw agent workspace with persistent community memory, identity files, and update scripts. The resulting agent can answer questions about community history, culture, channels, and recurring patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill builds a persistent memory agent from Discord messages, which can preserve private or sensitive community content.

Mitigation: Review data-governance requirements before installation, restrict exports to authorized channels, and protect generated memory files as private Discord-derived data.

Risk: Server security evidence says advertised safety filtering is not enforced and unsafe Discord content may reach the agent memory flow.

Mitigation: Do not run cron or heartbeat updates until safety filtering is fixed, enforced, and verified against the SQLite content used for memory generation.

Risk: The workflow relies on sensitive Discord token handling.

Mitigation: Prefer a bot or OAuth-style token flow where possible, avoid browser user tokens, and tightly restrict access to any token file.

## Reference(s):

- [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [LanceDB Integration](references/lancedb.md)
- [Security Reference](references/security.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python and shell scripts, JSON configuration snippets, and generated agent workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Running the scripts can produce local SQLite databases and Markdown memory files containing Discord server content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
