## Description:

Sends Feishu text messages from local OpenClaw agent credentials so execution agents can report task results to a user or group chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and multi-agent workflow operators use this skill to let execution agents send completion reports to Feishu users or group chats under per-agent bot identities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local Feishu app credentials to send external messages automatically with weak scoping and input validation.

Mitigation: Install only in a controlled Feishu/OpenClaw environment, use narrowly scoped app credentials, confirm recipients and message content before autonomous use, and prefer a version that validates agent IDs and restricts receive_id_type.

Risk: Message payloads and credential metadata may be exposed through logs or unsafe payload construction.

Mitigation: Mask credential metadata in logs and use safe JSON encoding for message payloads before allowing production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pikaqiuyaya/skills/feishu-auto-report)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/)
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text]

**Output Format:** [Shell command invocation and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends text content to Feishu using agent-specific local app credentials.]

## Skill Version(s):

5.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
