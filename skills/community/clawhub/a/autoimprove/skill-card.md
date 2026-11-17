## Description:

Autoimprove runs an autonomous optimization loop that changes scoped project files, checks correctness, measures a score, and keeps only experiments that meet the configured goal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zanetworker](https://clawhub.ai/user/zanetworker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to optimize measurable software or AI system outcomes such as performance, cost, bundle size, model quality, prompt quality, SQL latency, CI speed, or infrastructure health. It guides setup, establishes a baseline, then iterates through scoped changes using tests, guards, scoring, commits, and rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs project-supplied shell commands and can inherit credentials from the agent process.

Mitigation: Run it with least-privilege credentials in an isolated clone, container, or disposable worktree, and remove secrets, production kubeconfigs, database credentials, and API tokens from the environment.

Risk: Headless runs can edit files, create commits, and reset repository history while pursuing the configured score.

Mitigation: Complete an interactive first run, review improve.md, verify the exact scope and commands, and confirm the backup branch and recovery process before any overnight or unattended execution.

Risk: Scope restrictions are policy constraints rather than a technical sandbox.

Mitigation: Use explicit scope and exclude rules, keep sensitive repositories in disposable forks or containers, and review diffs before accepting results.

Risk: Optimization pressure can encourage metric gaming or changes to evaluation guardrails.

Mitigation: Keep tests, eval scripts, golden sets, and scoring commands immutable during the loop, and use guard metrics for secondary regressions.

## Reference(s):

- [ClawHub Autoimprove Skill Page](https://clawhub.ai/zanetworker/skills/autoimprove)
- [Autoimprove Protocol](references/protocol.md)
- [Autoimprove Examples](references/examples.md)
- [From Autoresearch to Autoimprove](docs/index.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, shell commands, project file edits, and JSON experiment logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create improve.md, program.md, test or eval scaffolds, git commits, backup branches, and .autoimprove JSON records depending on the selected workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
