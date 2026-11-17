## Description:

Connect a Feishu (Lark) bot to Clawdbot via WebSocket long-connection. No public server, domain, or ngrok required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexanys](https://clawhub.ai/user/alexanys)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to set up, run, troubleshoot, and optionally auto-start a Feishu/Lark messaging bridge for a Clawdbot agent. It is suited for Feishu bot creation, credential setup, WebSocket bridge startup, service diagnostics, and group chat response tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reachable Feishu users can prompt the configured Clawdbot agent through the operator's local Gateway identity.

Mitigation: Use only trusted Feishu bots and chats, add tenant/chat/sender allowlists before broader use, and keep the configured agent's tools to the minimum needed.

Risk: The optional macOS LaunchAgent can keep the bridge running continuously after setup.

Mitigation: Run the bridge interactively first and enable the LaunchAgent only when an always-on bridge is required; review service logs and unload the service when it is no longer needed.

Risk: Messages sent through the bot may be relayed to the configured agent and its enabled tools.

Mitigation: Avoid sending secrets or regulated data through the bot and use chats with trusted members.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/app)
- [ClawHub Skill Page](https://clawhub.ai/alexanys/skills/feishu-bridge)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu bot setup steps, environment variable names, launchd service commands, diagnostics, and group chat behavior guidance.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
