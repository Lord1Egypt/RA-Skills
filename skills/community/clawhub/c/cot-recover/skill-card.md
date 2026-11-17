## Description:

Scan for orphaned worktrees and stale branches after crashes or abandoned sessions. Offers safe cleanup options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Git worktrees and branches after crashes, abandoned sessions, or routine cleanup windows. It reports candidate cleanup actions while keeping destructive steps gated on explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Git cleanup commands may include repository-controlled paths, branch names, refs, or commit hashes.

Mitigation: Review every generated command before execution and validate paths, refs, branch names, and commit hashes as literal arguments.

Risk: Approved cleanup actions can remove worktrees or branches and may discard unmerged commits or uncommitted changes if misclassified.

Mitigation: Keep scans read-only by default, inspect status and log output before cleanup, and prefer merge or cherry-pick over deletion unless discard is explicitly confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/cot-recover)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline Git shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only scan guidance by default; cleanup commands require explicit user approval.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
