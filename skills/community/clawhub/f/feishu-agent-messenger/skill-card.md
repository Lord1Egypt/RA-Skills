## Description:

Send messages via Feishu using the current agent's credentials, supporting private and group chats with independent agent identity display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let multi-agent workflows send Feishu private or group updates through each agent's configured Feishu app identity. It is intended for task completion reports, progress updates, and similar agent-to-user notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local Feishu app credentials and send outbound messages externally.

Mitigation: Install it only for agents that are allowed to access those credentials and send Feishu messages; lock down the OpenClaw config file and use least-privilege Feishu app scopes.

Risk: An automatic message.received hook can create unintended outbound replies without sufficient safeguards.

Mitigation: Do not enable the hook unless sender allowlists, rate limits, loop prevention, and message-review rules are in place.

Risk: Message and target values can be unsafe if passed into request JSON without validation and encoding.

Mitigation: Patch the script to validate msg_type and JSON-encode target and message values safely before sending requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pikaqiuyaya/skills/feishu-agent-messenger)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown instructions with shell, JSON, and JavaScript snippets; shell command status text when send.sh is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local OpenClaw Feishu configuration, jq, curl, and network access to Feishu APIs.]

## Skill Version(s):

1.0.5 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
