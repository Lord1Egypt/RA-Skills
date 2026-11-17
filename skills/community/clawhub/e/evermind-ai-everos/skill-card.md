## Description:

Installs and configures the EverOS OpenClaw context-engine plugin so OpenClaw can recall and save conversation memory through a self-hosted EverOS backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alwaysday1](https://clawhub.ai/user/alwaysday1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install EverOS persistent memory, configure the OpenClaw context-engine slot, connect to an EverOS backend, restart OpenClaw, and verify memory through natural-language conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin automatically persists conversation content to the configured EverOS backend.

Mitigation: Avoid sensitive conversations until logging, retention, deletion, and memory-review controls are acceptable for the deployment environment.

Risk: Installation modifies the local OpenClaw configuration and changes plugin slots.

Mitigation: Review changes to ~/.openclaw/openclaw.json before restarting OpenClaw.

Risk: Setup guidance includes remote install patterns and backend startup commands.

Mitigation: Pin the npm package to the reviewed version, avoid curl-to-shell setup where possible, and install only if EverMind, the package, and the configured backend are trusted.

Risk: Memory recalled from the backend is injected into the assistant context.

Mitigation: Keep the backend on localhost or HTTPS and review memory contents and backend trust boundaries before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alwaysday1/skills/evermind-ai-everos)
- [EverMemOS Backend](https://github.com/EverMind-AI/EverMemOS)
- [Evermemos OpenClaw Plugin Repository](https://github.com/EverMind-AI/evermemos-openclaw-plugin.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local OpenClaw configuration changes, backend health checks, gateway restart commands, and natural-language memory verification steps.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter, package.json, openclaw.plugin.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
