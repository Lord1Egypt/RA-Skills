## Description:

Installs, configures, and troubleshoots OpenClaw on Linux hosts with DingTalk, Feishu, Discord, additional documented channels, and Bailian/DashScope models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to provision OpenClaw gateways and configure DingTalk, Feishu, Discord, or newly discovered channel integrations on Linux hosts. It also guides model-provider mapping, health checks, troubleshooting, and evidence collection for reproducible setup work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root-level installation and privileged workspaces can broaden the impact of setup mistakes or compromised dependencies.

Mitigation: Run OpenClaw under a dedicated unprivileged service account, avoid using /root/ as the workspace, and inspect generated service definitions before enabling them.

Risk: Mutable package and plugin installs can change behavior between runs.

Mitigation: Pin and verify Node.js packages, OpenClaw releases, and channel plugins before deployment.

Risk: Messaging channels and bot credentials can expose the agent to broad user access if configured too openly.

Mitigation: Store secrets outside the agent workspace with restricted permissions and prefer pairing or allowlists for channel access.

Risk: Persistent gateway services may keep running with stale or insufficiently reviewed configuration.

Mitigation: Review configuration before restart, verify gateway health, and monitor logs after enabling the service.

## Reference(s):

- [Channel Discovery and Auto-Install Workflow](references/channel-discovery.md)
- [OpenClaw Configuration Reference](references/config.md)
- [DingTalk Bot Setup Guide](references/dingtalk-setup.md)
- [Discord Channel Setup Guide](references/discord-setup.md)
- [Feishu Channel Setup Guide](references/feishu-setup.md)
- [OpenClaw Channels Documentation](https://docs.openclaw.ai/channels/index)
- [DingTalk OpenClaw Connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector.git)
- [DingTalk Open Platform](https://open.dingtalk.com/)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Lark Open Platform](https://open.larksuite.com/app)
- [Discord Developer Portal](https://discord.com/developers/applications)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup validation, troubleshooting checks, and evidence collection steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
