## Description:

Delegates heavyweight coding tasks to Claude Code for code review, module generation, complex debugging, and architecture design while the primary agent coordinates and validates the work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turnpound](https://clawhub.ai/user/turnpound)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide when and how to delegate substantial coding work to Claude Code CLI, including reviews, code generation, debugging analysis, and architecture planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates recommend running Claude Code with permission checks bypassed and project write access.

Mitigation: Remove bypassPermissions by default, use read-only review modes where possible, and grant write access only after the task scope is explicit.

Risk: Broad project paths such as the current working directory can expose more files than the task requires.

Mitigation: Use the smallest explicit project path or file set needed for the delegated task.

Risk: Delegated coding outputs may include incorrect recommendations or unsafe file changes.

Mitigation: Inspect outputs and diffs before accepting changes, then run the relevant tests or build checks.

## Reference(s):

- [Server-resolved source repository](https://github.com/TURNPOUND/claude-code-skill)
- [ClawHub skill release](https://clawhub.ai/turnpound/skills/claude-code-skill-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Claude Code CLI and is marked for Windows in ClawHub metadata.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
