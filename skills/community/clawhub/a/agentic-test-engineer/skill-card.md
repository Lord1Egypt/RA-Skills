## Description:

Generates and maintains unit, integration, and end-to-end tests, diagnoses flaky tests, suggests selector repairs, and reviews test coverage for QA engineers and developers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this advisory skill to draft tests, analyze flaky failures, propose selector updates, and triage coverage gaps for review in their own environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because three local references could not be resolved.

Mitigation: Resolve or inspect those references before relying on the skill; a benign scan verdict does not establish that unresolved content is risk-free.

Risk: Screenshots, DOM snapshots, or test data may leave the network when an external visual-testing or self-healing service is used.

Mitigation: Use synthetic test data, redact sensitive content, and review the vendor's data handling before enabling uploads.

Risk: A suggested selector or generated assertion could target the wrong element or encode an incorrect expectation.

Mitigation: Review generated tests and selector changes against the specification, and require human approval before merging.

## Reference(s):

- [Agentic Test Engineer on ClawHub](https://clawhub.ai/gechengling/skills/agentic-test-engineer)

## Skill Output:

**Output Type(s):** [Code, Analysis, Guidance, Configuration]

**Output Format:** [Markdown with code snippets, selector examples, and structured test and analysis tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory drafts for human review; the skill does not execute tests or modify repositories.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
