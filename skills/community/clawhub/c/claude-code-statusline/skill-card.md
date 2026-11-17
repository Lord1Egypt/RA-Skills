## Description:

Install and configure a custom Claude Code status line showing real-time token usage, context window percentage, git branch, and color-coded warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to install and manage a local status line that displays model, token usage, context-window percentage, git branch, and warning colors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently changes Claude Code configuration and can overwrite an existing statusLine setting.

Mitigation: Review the commands before running them and back up ~/.claude/settings.json and ~/.claude/settings.local.json before install, configure, or uninstall operations.

Risk: Unexpected files or symlinks under ~/.claude could affect local configuration changes.

Mitigation: Inspect ~/.claude for symlinks or unexpected files before installing, and run install, configure, or uninstall only when those changes are intended.

## Reference(s):

- [Claude Code Statusline on ClawHub](https://clawhub.ai/ajitsingh25/skills/claude-code-statusline)
- [Publisher profile: ajitsingh25](https://clawhub.ai/user/ajitsingh25)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs and configures local Claude Code status line files under ~/.claude.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
