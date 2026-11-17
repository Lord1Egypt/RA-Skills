## Description:

Optimize Bun workspaces and monorepos - analyze dependency hoisting, script performance, build pipelines, and workspace configuration for maximum speed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze Bun workspaces and monorepos, identify dependency, build, test, CI, and migration improvements, and produce actionable optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested dependency, build, test, CI, and migration changes may be incorrect for a specific repository.

Mitigation: Review proposed file edits and validate recommendations against the workspace package metadata and CI requirements before applying them.

Risk: Lockfile removal, package manager migration, or install commands may disrupt non-Bun projects or existing workflows.

Mitigation: Confirm the project is intended to use Bun and review any lockfile, package manager, or install-command change before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/bun-workspace-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with shell commands, code snippets, configuration changes, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dependency audits, performance comparisons, migration steps, and CI or workspace configuration recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
