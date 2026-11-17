## Description:

Builds a Discord AI command center server through the Discord REST API, including categories, channels, roles, and pinned workflow cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calecorbett](https://clawhub.ai/user/calecorbett)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create a structured Discord workspace for AI agent management, including operational channels, agent-specific channels, roles, and pinned workflow cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can make persistent Discord server changes using a bot token with server-management permissions.

Mitigation: Run against a test or empty guild first, verify the guild ID, review the dry-run preview, and get explicit confirmation before a live run.

Risk: Passing a Discord bot token on the command line can expose it through shell history or logs.

Mitigation: Avoid exposing the token in logs or command history and rotate the token if it may have been exposed.

Risk: Channel permissions may not match the intended private or readonly posture after creation.

Mitigation: Manually verify channel permissions before storing sensitive agent outputs or personal content in the server.

Risk: Re-running after a partial failure can create duplicate channels because channel deduplication is not implemented.

Mitigation: Use dry-run before reruns and manually remove duplicate channels if a previous live run partially completed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calecorbett/skills/discord-hub-builder)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord API v10](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash commands and Python script execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent Discord server changes when run live.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
