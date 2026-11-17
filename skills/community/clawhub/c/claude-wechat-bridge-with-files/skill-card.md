## Description:

Helps an agent configure a Claude Code or OpenClaw bridge for receiving WeChat ClawBot messages, handling inbound media files, replying to users, and sending proactive text notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect Claude Code or OpenClaw to WeChat ClawBot for remote human-agent interaction, inbound file handling, and proactive task status messages. It is suited to workflows where the agent runs on a computer while the user interacts from mobile WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad real-world messaging capability through WeChat and can send proactive messages using local credentials.

Mitigation: Enable proactive sending only when that authority is acceptable, and stop the bridge when the workflow is complete.

Risk: The bridge stores and reuses local account credentials for WeChat access.

Mitigation: Use a dedicated WeChat account, protect the host system, and avoid sending secrets through the bridge.

Risk: Inbound files from WeChat are downloaded locally and exposed to the agent as file paths.

Mitigation: Treat received files as untrusted content and scan or inspect them before relying on their contents.

Risk: The skill depends on a third-party npm package and a development-channel loading flag.

Mitigation: Pin the npm package version, review updates before upgrading, and avoid long-running unattended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinadu-ai/skills/claude-wechat-bridge-with-files)
- [claude-wechat-channel npm package](https://www.npmjs.com/package/claude-wechat-channel)
- [claude-wechat-channel GitHub repository](https://github.com/fengliu222/claude-wechat-channel)
- [Tencent WeChat ClawBot article](https://cloud.tencent.com/developer/article/2644003)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, and helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for MCP setup, media patch installation, bridge troubleshooting, and proactive text sending.]

## Skill Version(s):

1.2.1 (source: server release evidence; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
