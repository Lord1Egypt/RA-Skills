## Description: <br>
Discord project collaboration infrastructure for OpenClaw agents. Manage Forum Channels, threads, participant permissions, and mention mode. Supports 3-tier architecture (Forum Channel -> Thread -> Default Channel) for multi-agent project coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemodigital](https://clawhub.ai/user/lemodigital) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create and manage Discord forum channels, project threads, agent participant permissions, and mention mode for multi-agent collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes ~/.openclaw/openclaw.json, including Discord bot token and channel permission mappings. <br>
Mitigation: Use a least-privilege Discord bot scoped to the intended guild and back up ~/.openclaw/openclaw.json before first use. <br>
Risk: Archive, remove, and permission commands can revoke agent channel access and trigger an OpenClaw gateway reload. <br>
Mitigation: Double-check destructive commands and participant lists before execution, especially in active project threads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lemodigital/discord-project-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/lemodigital) <br>
- [OpenClaw Repository](https://github.com/openclaw/openclaw) <br>
- [Discord API v10](https://discord.com/api/v10) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for Discord/OpenClaw project management actions and invokes CLI/API workflows that can update local OpenClaw configuration.] <br>

## Skill Version(s): <br>
2.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
