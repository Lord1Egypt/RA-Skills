## Description:

Use when needing to coordinate multiple AI agents in parallel for code development, testing, and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuchang8877](https://clawhub.ai/user/liuchang8877)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multiple Codex agents across isolated git worktrees for code implementation, testing, and review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded example worktree paths may not match the user's environment.

Mitigation: Review and replace local paths before running setup or task distribution commands.

Risk: Multiple Codex sessions may modify separate worktrees and consume normal Codex account resources.

Mitigation: Run agents only in intended worktrees, review diffs before merging, and monitor Codex usage.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific Codex commands and local worktree paths that must be adapted before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
