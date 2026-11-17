## Description:

A comprehensive skill for using the Cursor CLI agent for various software engineering tasks, updated for 2026 features and tmux-based automation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to install, authenticate, configure, and operate Cursor CLI for terminal-based AI coding workflows such as code review, refactoring, debugging, Git assistance, and CI-style batch analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a curl-to-shell installer path.

Mitigation: Prefer a package-managed or verified Cursor CLI installation path and review installer contents before execution.

Risk: The automation workflow can auto-trust workspaces or apply changes with force mode.

Mitigation: Do not auto-trust unknown workspaces and avoid `--force` except in isolated repositories with version control and reviewed scope.

Risk: Cursor CLI automation can hang when run without a real TTY.

Mitigation: Use a reviewed tmux-based workflow or another real TTY approach when running from agents, scripts, or CI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/abe-cursor-agent)
- [Cursor CLI installer](https://cursor.com/install)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes interactive and non-interactive Cursor CLI workflows; command execution depends on local CLI setup and credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter states 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
