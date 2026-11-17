## Description:

Run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent via background process for programmatic control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratiknarola](https://clawhub.ai/user/pratiknarola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run and monitor coding agents in background sessions, especially for non-interactive coding tasks and batch review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes workflows for unsandboxed autonomous agent execution.

Mitigation: Use sandboxed or manual-approval modes by default, and reserve --yolo-style execution for isolated disposable environments.

Risk: The skill includes workflows that can automatically commit, push, or publish changes.

Mitigation: Review agent output before publishing and run these workflows only in intentionally scoped repositories or worktrees.

Risk: The skill includes mutable dependency installation steps.

Mitigation: Inspect dependency installation commands before running them and prefer controlled environments for execution.

Risk: The skill contains fixed third-party PR attribution text.

Mitigation: Remove or override fixed attribution before publishing anything under a different account.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one supported agent binary: claude, codex, opencode, or pi.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
