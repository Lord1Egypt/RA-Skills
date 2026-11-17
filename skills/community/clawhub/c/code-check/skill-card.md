## Description:

Run project quality checks and security reviews, fixing all errors by priority until all pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run linting, type checks, tests, security audits, formatting, and build checks, then fix reported issues until the project checks pass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to edit repository files while resolving check failures.

Mitigation: Use it in trusted repositories and explicitly request diagnostic-only behavior when code changes are not desired.

Risk: Automated fixes may change behavior while addressing lint, test, build, or security findings.

Mitigation: Review the resulting diff and re-run the relevant project checks before relying on the changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify repository files to resolve issues reported by project checks; does not commit code or change version numbers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
