## Description: <br>
Complete A-Z Discord server administration for channel, role, member, AutoMod, webhook, template, audit log, scheduled event, thread, and server control via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheBigBrainChad](https://clawhub.ai/user/TheBigBrainChad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Discord server administrators and automation-focused developers use this skill to operate a Discord server through shell commands, including moderation, channel and role management, AutoMod configuration, webhooks, audit logs, events, templates, and thread operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Discord server-changing power with few built-in safeguards. <br>
Mitigation: Install it only when intentional, use a dedicated least-privilege bot limited to the intended guild, and manually review delete, ban, kick, webhook, role, guild-setting, and bulk commands before execution. <br>
Risk: Discord bot tokens can be exposed through command lines, logs, or shared shell history. <br>
Mitigation: Provide tokens through a protected environment or secret store, avoid passing tokens as command-line arguments, and keep tokens out of logs and shared shells. <br>


## Reference(s): <br>
- [Discord API v10](https://discord.com/api/v10) <br>
- [ClawHub skill page](https://clawhub.ai/TheBigBrainChad/discord-admin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with bash command examples, shell scripts, and JSON API payloads or responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Discord bot token and Discord server, channel, role, message, and user identifiers; command effects depend on bot permissions and Discord API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
