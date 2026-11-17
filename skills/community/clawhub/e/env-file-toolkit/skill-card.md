## Description:

Manage .env files with validate, diff, template generation, merge, and missing-key checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, compare, template, merge, and check .env files across local, staging, and production environment configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles secret-bearing .env files and can display or preserve sensitive values through diff output, value listing, template generation with kept values, merge output, or stdout.

Mitigation: Use value-revealing options only in a controlled local context, review outputs before sharing, and do not commit generated files that preserve real secrets.

Risk: Merged or generated env files can be unsafe to source directly if values have not been reviewed and safely quoted.

Mitigation: Review generated files before using them in shell workflows and safely quote values before sourcing or deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and file-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated .env.example or merged .env files when the user requests file creation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
