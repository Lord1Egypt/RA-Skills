## Description:

Effective Git helps agents analyze changes, prepare commits, push safely, rebase or merge, and guide conflict resolution using Git best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guguoyi](https://clawhub.ai/user/guguoyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage everyday Git workflows, including reviewing diffs, selecting commit strategy, writing commit messages, pushing current branches, and resolving merge conflicts with user-reviewed decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Git commands that change repository history or working-tree state, including commit, amend, stash, checkout, reset, rebase, clean, and push workflows.

Mitigation: Review diffs before commits and require explicit confirmation before push, amend, reset, clean, rebase, force push, or any operation that rewrites history.

Risk: Quick commands include mutating operations, so users may assume the shorthand mode is read-only when it is not.

Mitigation: Use the explicit gq prefix only for intended actions and confirm branch, status, and target operation before running quick commit, branch, stash, or checkout commands.

Risk: Diff display behavior can depend on PAGER, GIT_QUICK_DIFF_PAGER, or GIT_QUICK_DIFF_TERMINAL values from the environment.

Mitigation: Use trusted pager and terminal environment values, or unset them and review diffs directly in the current terminal.

Risk: Conflict resolution can lose code if one side is kept without understanding both changes.

Mitigation: Save a pre-merge snapshot, present both sides when uncertain, and require user approval before choosing ours, theirs, or a rewritten resolution.

## Reference(s):

- [Effective Git README](README.md)
- [Git Best Practices](references/best-practices.md)
- [Conflict Resolution Guide](references/conflict-resolution.md)
- [Quick Git Commands Reference](references/quick-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run Git commands; destructive operations require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
