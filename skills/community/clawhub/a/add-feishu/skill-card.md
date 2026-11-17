## Description:

Add Feishu (Lark) as a channel using a WebSocket long connection, with no public URL or ngrok required, alongside WhatsApp, Telegram, Slack, or as a standalone channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[will-17173](https://clawhub.ai/user/will-17173)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add and configure a Feishu/Lark messaging channel for NanoClaw. It applies code changes, guides app setup, configures credentials, and explains registration and troubleshooting for direct and group chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu App Secret credentials and instructs users to copy runtime environment files, which can expose secrets if files are committed, backed up, or included in diagnostics.

Mitigation: Use a dedicated runtime env file containing only FEISHU_APP_ID and FEISHU_APP_SECRET, restrict file permissions, and keep credential files out of version control, backups, and diagnostics.

Risk: The requested Feishu permissions include im:chat.members:read, which the security summary flags as apparently unused.

Mitigation: Remove im:chat.members:read unless review confirms it is required for the deployment.

Risk: Registered Feishu chat messages, sender identity, and chat metadata are processed and stored by NanoClaw so the bot can respond.

Mitigation: Review data handling expectations before enabling the channel, register only intended chats, and test with a pinned or local install before broader deployment.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)
- [Lark Open Platform](https://open.larksuite.com)
- [Feishu Bot Info API](https://open.feishu.cn/open-apis/bot/v3/info)
- [ClawHub skill page](https://clawhub.ai/will-17173/skills/add-feishu)
- [Publisher profile](https://clawhub.ai/user/will-17173)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic code package instructions, environment variable guidance, validation commands, chat registration snippets, troubleshooting steps, and removal guidance.]

## Skill Version(s):

1.0.0 (source: manifest.yaml and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
