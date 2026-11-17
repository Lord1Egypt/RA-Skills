## Description:

为多个 OpenClaw Agent 配置独立的飞书机器人，支持免配对直接聊天模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitxuzhefeng](https://clawhub.ai/user/gitxuzhefeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure multiple OpenClaw agents with separate Feishu bot credentials, apply the gateway configuration, verify service status, and return a concise setup summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Open direct-message and group access can allow reachable Feishu users or groups to talk to connected agents without pairing.

Mitigation: Use this posture only intentionally; prefer allowlists or pairing where possible and restrict each connected agent's tools.

Risk: Feishu App Secrets are collected and written into persistent gateway configuration.

Mitigation: Protect App Secrets, avoid logging or sharing them, and confirm the exact configuration patch before applying it.

Risk: Persistent gateway changes trigger a restart and may affect existing bot connectivity.

Mitigation: Keep rollback instructions available and verify service health with openclaw gateway status after applying the patch.

## Reference(s):

- [OpenClaw Feishu documentation](https://docs.openclaw.ai/channels/feishu.md)
- [ClawHub skill page](https://clawhub.ai/gitxuzhefeng/skills/feishu-multi-bot)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with JSON configuration and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles Feishu App IDs and App Secrets; output should avoid exposing secrets in logs or public summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
