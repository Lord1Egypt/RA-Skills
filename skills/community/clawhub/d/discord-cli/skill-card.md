## Description:

Discord CLI gives agents structured terminal access to fetch Discord chat history, search messages, sync channels, export local data, and request AI analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwener](https://clawhub.ai/user/jackwener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate the discord-cli command-line tool for local-first Discord message sync, search, export, and summarization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent access to a sensitive Discord user token and may save it in a plaintext .env file.

Mitigation: Use only accounts and servers where automation is allowed, avoid discord auth --save unless local plaintext storage is acceptable, and protect or remove any saved token.

Risk: Broad sync and summary commands can cache or process large amounts of accessible Discord message content.

Mitigation: Prefer channel-specific commands, small -n limits, and explicit export destinations; avoid sync-all or broad summaries unless that scope is intended.

Risk: AI analysis and summary commands can send raw chat content to Anthropic.

Mitigation: Do not run AI commands on private, confidential, or regulated channels unless participants and organizational policy permit external processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackwener/skills/discord-cli)
- [Structured Output Schema](./SCHEMA.md)
- [README](./README.md)
- [PyPI package](https://pypi.org/project/kabi-discord-cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI results are YAML or JSON structured envelopes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agents should prefer bounded result sets, structured output, and file export for large datasets.]

## Skill Version(s):

0.2.3 (source: ClawHub release evidence and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
