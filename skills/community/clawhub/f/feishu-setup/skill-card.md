## Description:

Guides OpenClaw users through Feishu app creation, openclaw-lark plugin installation, OAuth scopes, event subscriptions, configuration, tool enablement, permission verification, and connectivity troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangzhipengdamon-maker](https://clawhub.ai/user/liangzhipengdamon-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure an OpenClaw instance for Feishu/Lark messaging, OAuth authorization, event subscriptions, plugin installation, and Feishu tool access. It is intended for setup and troubleshooting guidance rather than direct automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide recommends broad Feishu permissions and many Feishu tools, including user-identity, message history, search, batch authorization, and write-capable operations.

Mitigation: Start with an IM-only scope and tool set, enable additional scopes only for a documented business need, and restrict rollout to test users or departments first.

Risk: The guide uses mutable plugin install commands that may resolve to different package versions over time.

Mitigation: Use pinned, verified plugin versions and review package provenance before installation.

Risk: The integration depends on webhook endpoints, app secrets, and stored OAuth tokens.

Mitigation: Secure the webhook endpoint, store secrets and tokens with an approved secret provider, and disable user-identity sending, chat history/search, and batch authorization unless needed.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu Open Platform App Configuration](references/feishu-app-config.md)
- [OpenClaw Configuration Reference for Feishu](references/openclaw-config-reference.md)
- [Feishu Permission Scopes Reference](references/permissions-reference.md)
- [Feishu Tool Matrix](references/tool-matrix.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON5 configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions, configuration snippets, permission scope lists, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
