## Description:

Analyzes an existing project to produce a detailed, structured report on its architecture, patterns, technical debt, and key areas for downstream work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cankocakulak](https://clawhub.ai/user/cankocakulak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect existing repositories and produce a structured analysis artifact for downstream planning, product, and implementation agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project contents may be summarized into a local analysis document, including sensitive details if the analyzed repository contains them.

Mitigation: Use the skill only on repositories appropriate for local documentation and review the generated analysis before sharing it.

Risk: The skill creates or updates documentation under docs/.

Mitigation: Review the generated docs/[project-name]/analysis.md before committing or distributing the artifact.

## Reference(s):

- [Analyzer ClawHub listing](https://clawhub.ai/cankocakulak/skills/analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown document with a machine-readable YAML summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates docs/[project-name]/analysis.md as a downstream-agent reference artifact.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
