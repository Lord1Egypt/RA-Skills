## Description:

Validate .circleci/config.yml files for syntax, structure, security, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate, lint, audit, and inspect CircleCI pipeline configuration files before committing or running CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted CircleCI configuration content could affect human-readable terminal output.

Mitigation: Prefer JSON output for untrusted configs or review raw terminal output carefully until terminal-control escaping is added.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and validator output that may be text, JSON, or summary format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The validator supports full validation, quick checks, job listing, workflow graph output, JSON output, summary output, and strict mode.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
