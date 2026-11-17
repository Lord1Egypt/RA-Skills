## Description:

Cross-Branch Migration Audit helps agents audit module or feature migrations across Git branches by analyzing commits, dependencies, conflict risks, and migration checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynnchuan](https://clawhub.ai/user/kynnchuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before cross-branch module or feature migrations to find relevant commits, external dependencies, likely conflicts, and a safe migration order. It is also used during migration to diagnose compilation errors and produce post-cherry-pick review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect source branch, target branch, paths, commit lists, or search terms can produce an incomplete migration scope or misleading migration plan.

Mitigation: Confirm all audit inputs with the user before running the analysis and require human review of the discovered commit set.

Risk: Untrusted branch names, paths, or search values could be unsafe if inserted into shell commands through string interpolation.

Mitigation: Use safe argument handling, quote shell parameters, and avoid executing generated commands against untrusted repositories without review.

Risk: Generated overwrite or cherry-pick advice could damage target-branch changes if followed without review.

Mitigation: Review generated migration advice, inspect diffs before applying changes, and run compilation or tests after each migration phase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kynnchuan/skills/cross-branch-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command snippets, migration plans, checklists, and generated HTML audit reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce risk file lists, commit lists, CSV exports, Markdown migration plans, and docs/migration-audit-<timestamp>.html reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
