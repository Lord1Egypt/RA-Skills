## Description:

Plan complex codebase migrations, including framework upgrades, language transitions, architecture refactors, dependency analysis, effort estimation, migration path mapping, phased planning, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess migration scope, compare source and target stacks, estimate effort, plan phased execution, identify codemods, track progress, and document migration risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested codemod or npx commands can modify many repository files or pull unreviewed packages.

Mitigation: Pin tool versions, run from a clean git checkpoint, review package sources when appropriate, and inspect generated diffs before committing.

Risk: Migration plans and effort estimates are heuristic and may miss project-specific constraints.

Mitigation: Validate estimates with maintainers, CI results, dependency compatibility checks, and staged migration reviews.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include migration assessments, phased plans, effort estimates, codemod suggestions, progress tables, and risk notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
