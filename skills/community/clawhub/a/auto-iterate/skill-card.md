## Description:

Auto Iterate runs autonomous, metric-driven edit, run, evaluate, and keep-or-rollback loops to improve a user-specified target file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawzhang](https://clawhub.ai/user/sawzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Auto Iterate to optimize machine learning training, performance tuning, prompt experiments, or other measurable workflows. The skill repeatedly modifies one target file, runs the configured command, extracts a metric, and keeps or rolls back each experiment based on the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended experiment loops can run shell commands for an open-ended period.

Mitigation: Use an isolated branch or worktree, set explicit time and iteration limits, and review the run command before starting.

Risk: Rollback behavior can discard unrelated work if the worktree is not clean.

Mitigation: Start from a clean disposable branch, back up uncommitted changes, and keep the target file restriction explicit.

Risk: Untrusted run commands or metric extraction patterns can make the optimization loop unsafe or misleading.

Mitigation: Use trusted commands and extraction patterns, inspect run.log and results.tsv, and review kept changes before relying on them.

## Reference(s):

- [ClawHub Auto Iterate release page](https://clawhub.ai/sawzhang/skills/auto-iterate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status updates with inline shell commands, code edits, run logs, and TSV result tracking.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify one target file, create git commits, write results.tsv and run.log, and roll back unsuccessful commits.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
