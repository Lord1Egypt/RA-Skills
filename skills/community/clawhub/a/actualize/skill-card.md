## Description:

Reconcile the project's FPF state with recent repository changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hahamumu08](https://clawhub.ai/user/hahamumu08)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit recent repository changes against an FPF knowledge base, identify context drift, stale evidence, and decisions that may need review, and record a new actualization baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects repository diffs and FPF knowledge-base files as part of its maintenance audit.

Mitigation: Install and run it only in repositories where this inspection is intended and review the generated actualization findings before acting on them.

Risk: The skill may update .fpf/.baseline when recording a new actualization point.

Mitigation: Review .fpf/.baseline before committing if repository cleanliness or baseline provenance matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown report with inline shell commands and baseline configuration content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose updates to .fpf/context.md and writes or updates .fpf/.baseline when recording a new actualization point.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
