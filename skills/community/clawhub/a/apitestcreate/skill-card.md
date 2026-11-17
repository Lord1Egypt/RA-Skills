## Description:

Generates structured API test analysis documents from OpenAPI or Swagger specifications, simplified interface definitions, or natural-language API descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackbat1988](https://clawhub.ai/user/blackbat1988)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and API reviewers use this skill to turn interface specifications into review-ready test analysis documents covering parameters, business logic, responses, security, performance, compatibility, and common API testing pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional YAML parser dependency may change behavior or receive security updates over time.

Mitigation: Pin and audit PyYAML before production use.

Risk: Generated test analysis may contain incorrect, incomplete, or overly broad recommendations.

Mitigation: Review generated test plans before acting on them.

Risk: Suggested API, database, smoke, or load tests could affect live systems if run in the wrong environment.

Mitigation: Run suggested tests only where you have authorization and rollback controls.

## Reference(s):

- [README_EN.md](artifact/README_EN.md)
- [test-case-design.md](artifact/references/test-case-design.md)
- [common-pitfalls.md](artifact/references/common-pitfalls.md)
- [openapi-example.yaml](artifact/examples/openapi-example.yaml)
- [simple-example.md](artifact/examples/simple-example.md)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown test analysis document with structured sections and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated plans should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
