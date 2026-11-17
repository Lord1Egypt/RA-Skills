## Description:

Audit React, Vue, or Svelte component libraries to find unused components, inconsistent props, missing documentation, accessibility issues, missing tests, and naming convention violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-system maintainers use this skill to audit React, Vue, or Svelte component libraries for component usage, documentation, prop consistency, test coverage, accessibility patterns, and naming conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad local repository searches where it is invoked.

Mitigation: Run it only in repositories intended for component-library review and confirm that broad local searches are acceptable before installation or use.

Risk: Pattern-based grep results may miss dynamic imports, runtime accessibility issues, or project-specific conventions.

Mitigation: Treat findings as audit leads and verify them with project owners, tests, accessibility tooling, or framework-specific analysis before making changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, markdown, json, shell commands, guidance]

**Output Format:** [Text, Markdown, or JSON audit reports with local shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are based on local repository search patterns and may need human verification.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
