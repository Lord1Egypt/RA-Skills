## Description:

Detects and reports unused exports, unreferenced files, and unused npm dependencies in JavaScript and TypeScript projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit JavaScript and TypeScript projects for potentially unused code and dependencies before manual cleanup. Findings should be reviewed before deleting code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may produce false positives or miss references in projects with dynamic imports, custom path aliases, barrel exports, monorepos, or externally consumed library exports.

Mitigation: Treat results as review candidates, verify each finding in source control, and run the project's tests before removing code.

Risk: The skill description includes removal-oriented language, while the inspected behavior is a read-only reporting helper.

Mitigation: Use the skill to identify candidates for cleanup, and keep deletion as a separate manual change reviewed by a developer.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON scanner report with suggested follow-up commands and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only local analysis; JSON output is available when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
