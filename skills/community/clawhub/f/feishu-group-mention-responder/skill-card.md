## Description:

在飞书群中，当机器人被@提及或接收到直接消息时，自动进行回复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorpha](https://clawhub.ai/user/lorpha)

### License/Terms of Use:


## Use Case:

External and developer users use this skill to help an agent recognize Feishu direct messages or group @mentions and send a concise reply to the sender. It is intended for Feishu group-chat bot interaction where the agent must identify mentions, avoid duplicate replies, and respond in Chinese by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot may read Feishu chat events and send messages as the bot in chats where it is installed.

Mitigation: Before installation, confirm the Feishu bot should have chat event access and send-as-bot permissions for the target workspace.

Risk: Default replies are Chinese and may not fit multilingual workspaces.

Mitigation: Adjust the default response language and wording before deployment if the workspace requires multilingual responses.

Risk: Mention detection or reply logic can cause duplicate or looping responses if bot identities and handled message IDs are not tracked correctly.

Mitigation: Configure reliable bot ID/name detection and suppress replies to non-mentions, already processed messages, and the bot's own messages.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with JSON and Python-like code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for Feishu message handling, mention detection, reply construction, and required bot permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
