## Description:

Manage AI configuration for OpenClaw, OpenCode, Codex CLI, and Claude Code, including provider and model changes and supported config file updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkuiwu](https://clawhub.ai/user/mkuiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to translate natural-language or structured requests into supported configuration actions for OpenClaw, OpenCode, Codex CLI, and Claude Code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently rewrite sensitive agent settings and credentials.

Mitigation: Use it only for deliberate AI configuration changes and inspect diffs before full-file replacements.

Risk: Provider credentials may be exposed through command-line arguments or generated configuration files.

Mitigation: Avoid passing real secrets as command-line arguments and check permissions on generated config files.

Risk: Backup files may retain old or rotated credentials.

Mitigation: Review and remove old backups that may contain sensitive credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkuiwu/skills/ai-config-admin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON/TOML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create backup files and rewrite supported local JSON/TOML agent configuration files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
