## Description:

Pushes backend API definition data to a product data platform for centralized API documentation management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowzhouj](https://clawhub.ai/user/snowzhouj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare, validate, and push Java API definitions, OpenAPI-style JSON, or controller-derived interface data to a product data platform and record push history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pushes potentially sensitive API documentation to a hardcoded external HTTP endpoint.

Mitigation: Review the destination before use, require HTTPS and a trusted authenticated endpoint, and do not send confidential, production, credential-bearing, or customer-sensitive API definitions.

Risk: Optional Git workflow automation can send API data during git operations.

Mitigation: Avoid installing the pre-push hook unless the team explicitly wants automatic submissions and requires approval controls before each push.

## Reference(s):

- [Product Platform API Docs](references/product-platform-api-docs.md)
- [API Definition Standard](references/api-definition-standard.md)
- [Push History](references/push-history.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute or propose HTTP API pushes when the user provides PRD and API definition inputs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
