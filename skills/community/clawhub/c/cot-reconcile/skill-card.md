## Description:

Tripwire check for multi-session drift. Scans state files, recent commits, and file conflicts caused by parallel Claude Code sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to check for branch, file, state, and single-source-of-truth drift after parallel Claude Code sessions, worktree merges, crashes, or heavy concurrent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect recent commit history and project state files when repository drift is suspected.

Mitigation: Use it in repositories where read-only inspection of history and state logs is acceptable, especially for private or sensitive projects.

Risk: Proposed reconciliation fixes may be incorrect when parallel sessions had different valid goals.

Mitigation: Review each proposed fix before approval and prefer evidence of intent over timestamps when resolving conflicts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/cot-reconcile)
- [Skill instructions](artifact/SKILL.md)
- [Readme](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with shell command snippets and proposed fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only scan by default; file changes are proposed for approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
