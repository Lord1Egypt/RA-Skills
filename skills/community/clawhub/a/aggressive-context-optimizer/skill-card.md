## Description:

Slash OpenClaw token costs and prevent context overflow by diagnosing expensive context sources and providing concrete configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omaression](https://clawhub.ai/user/omaression)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to reduce OpenClaw token usage, troubleshoot context overflow, and tune OpenClaw configuration for leaner long-running sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently rewrite OpenClaw configuration after broad cost or context triggers.

Mitigation: Review proposed changes before using --apply, especially --apply --aggressive, and validate configuration after changes.

Risk: Aggressive context limits may reduce memory recall quality, prune useful tool output, or affect future session behavior.

Mitigation: Re-check /status and /usage tokens, spot-check representative recall, and loosen the most recent change if quality drops.

## Reference(s):

- [Aggressive all-in-one config](references/aggressive-config.md)
- [Commands cheat sheet](references/commands.md)
- [Config examples](references/configs.md)
- [ClawHub skill page](https://clawhub.ai/omaression/skills/aggressive-context-optimizer)
- [Publisher profile](https://clawhub.ai/user/omaression)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent OpenClaw configuration changes that should be reviewed before applying.]

## Skill Version(s):

1.0.0-alpha (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
