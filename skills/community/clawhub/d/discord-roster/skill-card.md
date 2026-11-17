## Description:

Query Discord guild members, list bots, and inspect channel and role information through the Discord REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1587causalai](https://clawhub.ai/user/1587causalai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to audit Discord server rosters, list bot or human members, and inspect guild channels, roles, and channel ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted arguments or environment values may cause unintended local code execution in the bundled script.

Mitigation: Review before installing, invoke only with trusted arguments and configuration, and fix the script to pass inputs to Python as data before routine use.

Risk: The skill uses a Discord bot token and can expose server roster, role, and channel information available to that bot.

Mitigation: Use a least-privilege bot token scoped to authorized guilds and store it only in the expected local configuration.

Risk: Proxy configuration can affect where Discord API traffic is routed.

Mitigation: Use only trusted proxy settings and verify the local configuration or environment before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1587causalai/skills/discord-roster)
- [Publisher Profile](https://clawhub.ai/user/1587causalai)
- [Discord REST API v10](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Tab-separated text and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Discord bot token and network access to Discord; supports optional proxy configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
