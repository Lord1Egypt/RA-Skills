## Description:

飞书多端机器人群聊对话中继 (Multi-Agent Relay)。通过后台轮询飞书群消息历史，监听对方机器人发言并代表本机机器人自动回复，实现多机器人在群内围绕指定话题的持续对话。

This skill is ready for commercial/non-commercial use.

## Publisher:

[puddy3133](https://clawhub.ai/user/puddy3133)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Feishu workspace operators use this skill to configure and run two Feishu bots that relay a controlled group-chat discussion through OpenClaw. It supports topic locking, pause/resume commands, round limits, and daemon status control for small-group multi-agent conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad group-chat participants can influence relay control phrases and automated posting behavior.

Mitigation: Use the skill only in restricted test groups until sender authorization, command namespacing, and round-limit controls are reviewed.

Risk: The relay handles Feishu app credentials, OpenClaw tokens, and conversation state.

Mitigation: Keep the runtime configuration out of source control, use narrowly scoped tokens, and protect local state and log files with restrictive permissions.

Risk: Configurable endpoints and automated posting can expose sensitive conversation flow if deployed on untrusted infrastructure.

Mitigation: Keep the OpenClaw endpoint on trusted loopback or HTTPS infrastructure and review the configuration before using the skill in real Feishu groups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/puddy3133/skills/feishu-multi-agent-replay)
- [Feishu Tenant Access Token OpenAPI](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu IM Messages OpenAPI](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions and commands for a Feishu multi-agent relay; runtime behavior depends on user-provided Feishu and OpenClaw credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
