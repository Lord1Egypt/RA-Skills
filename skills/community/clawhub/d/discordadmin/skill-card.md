## Description:

Complete A-Z Discord server administration. Channel/role/member management, AutoMod, webhooks, templates, audit logs, scheduled events, threads, and full server control via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebigbrainchad](https://clawhub.ai/user/thebigbrainchad)

### License/Terms of Use:


## Use Case:

External developers and Discord server administrators use this skill to manage Discord servers from a command-line interface, including channels, roles, members, moderation actions, webhooks, templates, audit logs, events, and bulk operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can perform destructive Discord server actions such as deleting channels, deleting messages, kicking users, banning users, and changing roles without safety confirmations.

Mitigation: Manually review each destructive command before execution and run the skill only in environments where operators are authorized to make the requested server changes.

Risk: A Discord bot token with broad permissions can expose substantial server control if mishandled locally.

Mitigation: Use a least-privileged bot, prefer the DISCORD_BOT_TOKEN environment variable over command-line token arguments, and run the scripts only on trusted machines with restricted process visibility.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thebigbrainchad/skills/discordadmin)
- [Discord API v10](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Discord bot token and Discord permissions appropriate to the requested administrative action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
