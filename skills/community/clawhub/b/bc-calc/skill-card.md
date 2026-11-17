## Description:

This skill evaluates arithmetic expressions using the Unix `bc` calculator with full `bc` syntax and arbitrary-precision calculation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danstaal](https://clawhub.ai/user/danstaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other users use this skill to calculate basic or advanced arithmetic expressions through an agent, including full `bc` syntax and math-library functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted `bc` programs from user input can hang or exhaust a worker.

Mitigation: Install only in trusted environments, or add strict expression validation, input/output caps, and a subprocess timeout before using untrusted or automated inputs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text calculation results or `bc` error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the `bc` math library by default.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
