## Description:

Delegates coding work to Codex, Claude Code, OpenCode, or Pi agents through bash commands, with guidance for foreground, background, PTY, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate feature work, refactoring, iterative implementation, and pull request review to coding-agent CLIs while keeping the agent focused on a target work directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated coding agents may run commands, modify files, or act with broad local authority, especially when approval or sandbox controls are disabled.

Mitigation: Use sandboxed modes, disposable clones or containers, pinned dependencies, and human review before commits, pushes, pull request comments, or commands that use local credentials.

Risk: The skill recommends workflows involving disabled approvals or sandboxing for some agents.

Mitigation: Install and use the skill only with explicit supervision policies and prefer the least-privileged execution mode that still supports the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/ai-coding-delegate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and workflow tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one compatible coding-agent CLI: claude, codex, opencode, or pi.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
