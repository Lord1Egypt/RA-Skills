## Description:

Creates and configures Scout, a proactive research assistant agent with Telegram integration, research tools, memory search, inter-agent collaboration, and skill provisioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure an OpenClaw research assistant agent with Telegram access, web research tools, memory search, skill discovery, and collaboration settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Telegram access can expose the agent to untrusted messages or unauthorized users.

Mitigation: Replace the Telegram allowlist with the installer's verified user ID and keep direct-message access allowlisted.

Risk: Bot tokens and related credentials can leak through shell history or shared configuration.

Mitigation: Use protected secret storage or environment injection for tokens, and avoid pasting bot tokens directly into shell commands.

Risk: Broad workspace, memory, search, and session permissions can expose unrelated data or agent sessions.

Mitigation: Use a Scout-specific workspace and memory namespace, enable only the tools Scout needs, and review session allowlists before deployment.

## Reference(s):

- [OpenClaw Agent Configuration](https://docs.openclaw.ai/concepts/agents)
- [Telegram Bot Setup](https://docs.openclaw.ai/channels/telegram)
- [Skill Discovery SOP](/skills/skill-discovery-sop)
- [Browser Automation Core](/skills/browser-automation-core)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command blocks and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholder secrets and allowlist values that users must replace before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
