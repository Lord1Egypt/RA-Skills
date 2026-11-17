## Description:

Debug Master provides Chinese-language debugging guidance using a seven-step method, root-cause analysis, automated test-case suggestions, error-pattern recognition, and cross-language troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windy-001-crypto](https://clawhub.ai/user/windy-001-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose programming errors, analyze root causes, generate regression test ideas, and structure debugging reports across common programming languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad debugging phrases and produce fixes or tests that have not been validated against the user's codebase.

Mitigation: Review generated tests and fixes before applying them, and run the project's normal test suite after changes.

Risk: Debugging logs can contain secrets such as API keys or tokens.

Mitigation: Redact credentials and other sensitive values before sharing logs with the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/windy-001-crypto/skills/debug-master)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with code blocks, shell command examples, debugging reports, fix suggestions, and test-case examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before applying fixes or tests to a codebase.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
