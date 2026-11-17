## Description:

Use when a task adds, upgrades, removes, or reviews software dependencies and the agent should apply a Socket-based supply-chain guardrail before changing manifests or lockfiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuthan](https://clawhub.ai/user/tuthan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review proposed dependency additions, upgrades, removals, and transient install commands before changing manifests or lockfiles. It guides agents through Socket-based review, policy checks, and safer alternatives or human review when risk signals are weak.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Socket-based reviews may perform external dependency lookups.

Mitigation: Install only when external package lookups are acceptable for the workspace, and prefer MCP depscore or a pinned, reviewed Socket CLI version.

Risk: The CI example uses credentialed GitHub execution and installs the Socket CLI dynamically.

Mitigation: Pin the CLI and GitHub Actions versions, reduce GitHub token permissions to the minimum needed, and review secrets handling before copying the workflow.

Risk: The helper script can write reports to a user-provided output path.

Mitigation: Avoid arbitrary or sensitive output paths and keep generated reports in a project-local review directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tuthan/skills/dependency-guard)
- [Canonical Policy](references/policy.md)
- [Decision Matrix](references/decision-matrix.md)
- [Example Review Format](references/examples.md)
- [GitHub Actions Example](examples/github/dependency-guard.yml)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Socket CLI authentication or MCP depscore availability before producing a dependency decision.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
