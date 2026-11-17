## Description:

conduxt orchestrates full-duplex coding agent sessions via ACPX or tmux, composing OpenClaw tools and community skills for implementation, bug fixes, refactoring, and investigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuezhouyang](https://clawhub.ai/user/xuezhouyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use conduxt to coordinate coding-agent sessions for feature implementation, bug fixes, refactoring, investigations, progress checks, cleanup, and PR-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended broad approvals can allow downstream coding agents to change repository files and run shell workflows without interactive review.

Mitigation: Require explicit confirmation before using --approve-all and before allowing git push or gh pr create in sensitive repositories.

Risk: The skill can create worktrees, branches, agent sessions, and persistent task-state files.

Mitigation: Use isolated worktrees and review generated state files before relying on them for project status or cleanup.

Risk: Adapter or agent behavior may change if ACP adapter versions are not pinned.

Mitigation: Pin ACP adapter versions and validate the workflow in a disposable repository before normal use.

Risk: Server security guidance calls out setup.sh Python fallback and Markdown escaping issues for sensitive repositories.

Mitigation: Fix those script issues or disable the helper scripts before installing the skill in repositories with sensitive code or credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuezhouyang/skills/conduxt)
- [conduxt Homepage](https://github.com/xuezhouyang/conduxt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON callback examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update worktrees, branches, task-state files, agent sessions, commits, pushes, and pull requests when the downstream environment permits those actions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
