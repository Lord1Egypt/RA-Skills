## Description: <br>
Discord server management CLI for managing channels, roles, permissions, messages, embeds, file uploads, emojis, invites, audit logs, and server settings with one command per API call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibbybuilds](https://clawhub.ai/user/ibbybuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to manage Discord servers from a terminal through the discli command line tool. It supports routine administration tasks such as channel, role, permission, message, invite, emoji, audit-log, and server-setting changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read Discord channel context and create persistent local persona state in ~/.discli/SOUL.md. <br>
Mitigation: Confirm the Discord permissions granted to the bot, avoid broad private-channel access unless needed, and inspect or remove generated SOUL.md content if it should not influence later behavior. <br>
Risk: Discord administration commands can change or delete server resources when used with sufficient permissions. <br>
Mitigation: Use dry-run previews where available, require explicit human review before destructive actions, and reserve --confirm for approved changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibbybuilds/discli) <br>
- [Discli homepage](https://github.com/ibbybuilds/discli) <br>
- [Discli bot setup documentation](https://github.com/ibbybuilds/discli/blob/master/docs/BOT_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI results may be YAML, JSON, or tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BOT_TOKEN and the discli binary; agent-facing CLI output defaults to YAML when piped.] <br>

## Skill Version(s): <br>
0.6.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
