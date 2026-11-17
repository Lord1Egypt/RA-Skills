## Description:

AI-powered monorepo management assistant for workspace orchestration, dependency management, and build optimization in large-scale monorepo projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermario11](https://clawhub.ai/user/supermario11)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect local JavaScript monorepo workspace packages and receive guidance for dependency analysis, build ordering, change detection, versioning, and CI/CD optimization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release description overstates the implementation: the included script is a simple local workspace package lister, not a full monorepo automation system.

Mitigation: Install only when that limited behavior is acceptable, and review generated guidance before relying on build optimization, versioning, or CI/CD claims.

Risk: The helper reads package metadata from the current working directory and workspace paths.

Mitigation: Run it only in intended, trusted repositories and review the listed packages before using the results in automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supermario11/skills/cuihua-monorepo-manager)
- [Publisher profile](https://clawhub.ai/user/supermario11)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print local workspace package names when the bundled Node.js helper is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
