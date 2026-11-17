## Description:

Guides agents in developing AstrBot plugins that match the AstrBot main repo, pass astr-plugin-reviewer checks, and cover commands, filters, hooks, LLM integrations, and agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camera-2018](https://clawhub.ai/user/camera-2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create or update AstrBot plugins with reviewer-compliant project structure, metadata, command handlers, message handling, LLM integrations, and publishing checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plugins generated with this guidance may include API keys, provider settings, or other sensitive configuration.

Mitigation: Review configuration schemas and README text before deployment, keep secrets user-provided, and avoid hard-coded credentials.

Risk: Persistent storage, proactive messages, and platform-specific APIs can affect user data or send messages outside an immediate command response.

Mitigation: Require user-requested behavior, document it clearly, store runtime data with AstrBot plugin data helpers, and guard platform-specific calls.

Risk: LLM hooks, LLM tools, and agent loops can modify prompts or take repeated tool-driven actions.

Mitigation: Review hook signatures, tool permissions, agent step limits, and user control points before enabling these features.

## Reference(s):

- [AstrBot Plugin Development](SKILL.md)
- [AstrBot Reviewer Checklist](references/reviewer-checklist.md)
- [AstrBot Plugin Project Structure](references/project-structure.md)
- [AstrBot Core API Reference](references/core-api.md)
- [AstrBot Advanced Features](references/advanced-features.md)
- [AstrBot Message Components](references/message-components.md)
- [AstrBot Reviewer-Friendly Patterns](references/patterns.md)
- [AstrBot Repository](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot Plugin Market](https://plugins.astrbot.app)
- [ClawHub Skill Page](https://clawhub.ai/camera-2018/skills/astrbot-plugin-dev-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, YAML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce plugin source files, metadata, configuration schemas, reviewer checklists, and command suggestions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
