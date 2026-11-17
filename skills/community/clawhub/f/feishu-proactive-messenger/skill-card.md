## Description:

Feishu Proactive Messenger sends text messages proactively through Feishu OpenAPI so OpenClaw agents can initiate outbound Feishu messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziwenwang28](https://clawhub.ai/user/ziwenwang28)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agent operators use this skill to let agents send proactive Feishu text messages from the correct configured bot account. It is useful in multi-agent workflows where an assigned agent needs to notify a user in its own Feishu chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callers have broad control over which configured bot identity sends messages and who receives them.

Mitigation: Restrict who can invoke the skill, constrain caller-controlled agent selection, and limit allowed recipients for each bot account.

Risk: The skill reads OpenClaw Feishu app credentials and uses them to send messages through configured bots.

Mitigation: Install only where this credential access is acceptable and isolate credentials per agent where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziwenwang28/skills/feishu-proactive-messenger)
- [Feishu tenant access token OpenAPI endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu send message OpenAPI endpoint](https://open.feishu.cn/open-apis/im/v1/messages)
- [Feishu bot info OpenAPI endpoint](https://open.feishu.cn/open-apis/bot/v3/info)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text status output with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends text-only Feishu messages using configured OpenClaw Feishu account credentials.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, clawdis.yaml, and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
