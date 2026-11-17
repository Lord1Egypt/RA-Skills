## Description:

Autoresearch.Bak guides an agent through setup, iterative one-variable experiments, metric extraction, git-backed result tracking, and analysis for measurable optimization tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run systematic optimization experiments where a single metric determines whether each code or configuration change is kept, discarded, or treated as a crash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an autonomous experiment loop indefinitely.

Mitigation: Set explicit experiment limits, time budgets, and stop conditions before running it.

Risk: The skill can edit code, run configured shell commands, create commits, and use destructive git resets.

Mitigation: Run it only in a disposable branch or worktree with a clean working tree, constrained target files, and reviewed run and extract commands.

Risk: Unrelated uncommitted work could be lost during experiment rollback.

Mitigation: Commit, stash, or move unrelated work before starting an autoresearch session.

## Reference(s):

- [Autoresearch Reference](artifact/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/lean-zhouchao/skills/autoresearch-bak)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration templates, and analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When followed by an agent, the skill may create autoresearch.config.md, results.tsv, a git branch, commits, run logs, and code or configuration edits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
