## Description:

Controls and manages Claude Code coding assistant workflows for project-aware coding, code review, refactoring, feature implementation, debugging, documentation, and OpenClaw ACP sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocherkong](https://clawhub.ai/user/rocherkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to launch and configure Claude Code for coding tasks, reviews, refactors, debugging, documentation generation, and isolated OpenClaw ACP sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a broad auto-approval Claude Code configuration that permits shell commands and file edits without per-action confirmation.

Mitigation: Review generated .claude/settings.json before use, prefer explicit approval or read-only settings for code review and untrusted repositories, and narrow allowed tools and directories to the task.

Risk: API keys or database credentials may be exposed if real secrets are placed in examples, committed configuration files, shell history, or logs.

Mitigation: Use environment variables or a secret manager for real credentials, keep examples as placeholders, and avoid committing or logging sensitive values.

Risk: Unpinned npm or npx tools can add supply-chain risk when installing or launching Claude Code-related tooling.

Mitigation: Pin, audit, or preinstall trusted npm packages before using the skill in sensitive projects.

## Reference(s):

- [Claude Code configuration reference](references/config-reference.md)
- [Claude Code workflow reference](references/workflows.md)
- [Claude Code documentation](https://docs.anthropic.com/claude-code)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/rocherkong/skills/claudecode-controller)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Claude Code CLI commands and create or update project-level .claude/settings.json configuration.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
