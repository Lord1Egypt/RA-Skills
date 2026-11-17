## Description:

Send a Feishu IM message as the app (bot identity). Use when you need to send a message that appears to come from the bot/app, not the user. Uses App Access Token (no user auth needed). Supports text, image, post, card, and other Feishu msg types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkzleond](https://clawhub.ai/user/jkzleond)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send Feishu messages through an app or bot identity for direct users or group chats, including text, image, post, card, and other Feishu message types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu app credentials and app access tokens.

Mitigation: Use a Feishu app with permissions limited to the intended messaging scope and run the skill as an unprivileged user.

Risk: Unsafe credential-loading and token-cache behavior could expose sensitive material.

Mitigation: Patch the script to pass OPENCLAW_JSON as an argument and store token cache data in a private chmod 600 user directory.

Risk: Messages are sent with bot/app identity to supplied recipient IDs.

Mitigation: Verify recipient IDs and message content before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkzleond/skills/feishu-send-message-as-app)
- [Feishu Open API base](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls, Configuration guidance]

**Output Format:** [Plain text message_id output and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials in openclaw.json and supports receive_id, msg_type, content, and receive_id_type inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
