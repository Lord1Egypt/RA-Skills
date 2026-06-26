## Description: <br>
Create a living agent from a Discord server that preserves community memory, voice, history, and culture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgeesawor](https://clawhub.ai/user/kgeesawor) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Community operators and developers use this skill to export Discord conversations, filter unsafe content, build an OpenClaw agent workspace, and maintain searchable community memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles full-server Discord message archives that may include private or sensitive community content. <br>
Mitigation: Use only with clear authorization, exclude sensitive channels where possible, and restrict access to exported data, SQLite databases, and generated memory files. <br>
Risk: The workflow depends on a Discord token and recurring storage of community data. <br>
Mitigation: Treat the Discord token like an account password, limit filesystem access to token and archive locations, and review retention practices before scheduled updates. <br>
Risk: The security evidence warns not to rely on the advertised safety pipeline until missing scripts and safe-only filtering are fixed. <br>
Mitigation: Review and repair the filtering workflow before ingestion, verify that only safe messages are used, and manually review third-party AI processing before enabling it. <br>


## Reference(s): <br>
- [ClawHub release](https://clawhub.ai/kgeesawor/discord-soul) <br>
- [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw) <br>
- [Security guide](references/security.md) <br>
- [LanceDB integration](references/lancedb.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and generated agent workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scripts and templates for exporting Discord messages, generating memory files, and configuring an OpenClaw agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
