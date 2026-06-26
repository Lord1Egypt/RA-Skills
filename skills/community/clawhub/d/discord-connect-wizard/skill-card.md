## Description: <br>
One-machine Discord bot onboarding wizard for OpenClaw. Use when setting up Discord for the first time (create bot, enable intents, invite to a guild, auto-write OpenClaw config, restart gateway, and complete DM pairing). Designed for local Mac/Windows/Linux hosts with a localhost web UI + optional browser automation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gm4leejun-stack](https://clawhub.ai/user/gm4leejun-stack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect a new Discord bot to a local OpenClaw installation with guided Discord setup, config writes, gateway restart, and pairing approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Discord bot token can control the bot if exposed. <br>
Mitigation: Treat the token like a password, avoid pasting it into chat unless necessary, do not log it, and reset it in Discord if exposure is suspected. <br>
Risk: The wizard writes OpenClaw Discord configuration and restarts the gateway. <br>
Mitigation: Review the generated accountId, server, and user before config is written, and run the skill only on the intended OpenClaw host. <br>
Risk: Setting requireMention=false may allow the bot to observe ambient messages in the allowed server. <br>
Mitigation: Use a private allowlisted server or change requireMention to true if ambient message handling is not desired. <br>


## Reference(s): <br>
- [Conversation Mode](references/conversation-mode.md) <br>
- [OpenClaw Discord Baseline](references/openclaw-discord-baseline.md) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Discord API v10](https://discord.com/api/v10) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local wizard UI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write OpenClaw Discord configuration and approve a Discord pairing when run by an agent with the required local permissions.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
