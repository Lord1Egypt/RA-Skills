## Description:

Bridge Discord messages to Agent Zero's HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wespeakallday](https://clawhub.ai/user/wespeakallday)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a Discord bridge that forwards allowed channel messages to Agent Zero and returns Agent Zero responses back to Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Discord audiences could invoke Agent Zero with the bridge's API authority if channel access is not restricted.

Mitigation: Run the bridge only in a dedicated, approved Discord channel and set DISCORD_CHANNEL_IDS explicitly.

Risk: Messages and credentials can be sent to configurable HTTP endpoints.

Mitigation: Use a least-privileged Agent Zero API key and keep the Agent Zero endpoint local or HTTPS-only.

Risk: Discord users may not expect their messages to be forwarded to Agent Zero.

Mitigation: Inform channel users that their messages are forwarded to Agent Zero before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wespeakallday/skills/discord-bridge)
- [Publisher profile](https://clawhub.ai/user/wespeakallday)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Discord text responses and Markdown setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discord responses are split to fit the 2000-character message limit.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
