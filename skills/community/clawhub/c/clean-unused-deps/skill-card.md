## Description:

Clean up unused npm dependencies in a project. Use when you want to remove packages that are installed but not used in the codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgxszhj-pixel](https://clawhub.ai/user/hgxszhj-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify unused npm dependencies, review the findings, and remove selected packages with npm uninstall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency cleanup can remove packages that are still needed through dynamic imports, scripts, configuration files, or framework conventions.

Mitigation: Treat depcheck output as a starting point, preserve the current project state first, review findings manually, uninstall in small batches, and run tests and builds after changes.

## Reference(s):

- [Clean Unused Deps on ClawHub](https://clawhub.ai/hgxszhj-pixel/skills/clean-unused-deps)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advises users to review dependency findings before uninstalling packages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
