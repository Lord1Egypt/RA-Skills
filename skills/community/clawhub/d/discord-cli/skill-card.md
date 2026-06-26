## Description: <br>
Discord CLI with YAML-first structured output for AI agents - fetch chat history, search messages, sync channels, and AI analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackwener](https://clawhub.ai/user/jackwener) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agents use this skill to operate discord-cli for local-first Discord message retrieval, search, export, syncing, and optional AI summarization. It is intended for accounts and machines the user controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recover and store a Discord user-session token. <br>
Mitigation: Use it only on accounts and machines you control, and avoid storing tokens in a project .env or sharing raw token values. <br>
Risk: Broad sync commands can create local archives of Discord messages across accessible channels. <br>
Mitigation: Review the channels that sync-all will collect and limit queries or sync scope where possible. <br>
Risk: AI analysis can send private message content to the configured AI provider. <br>
Mitigation: Use AI analysis only when you are comfortable sharing the selected message content with that provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackwener/discord-cli) <br>
- [Publisher profile](https://clawhub.ai/user/jackwener) <br>
- [Structured output schema](SCHEMA.md) <br>
- [PyPI package](https://pypi.org/project/kabi-discord-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, YAML] <br>
**Output Format:** [Markdown guidance with inline shell commands; invoked CLI commands can produce YAML or JSON envelopes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Machine-readable CLI output uses an ok/schema_version/data or error envelope; non-TTY stdout defaults to YAML.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
