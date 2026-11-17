## Description:

Generates professional Chinese API documentation from code, OpenAPI/Swagger specs, or endpoint descriptions, with terminology guidance, realistic examples, error-code tables, authentication sections, rate-limit sections, and optional backend validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to create native Chinese API reference documentation from OpenAPI/Swagger specs, source code, or plain-language endpoint descriptions. It is suited for Chinese developer-facing REST API docs that need consistent terminology, examples, authentication guidance, rate-limit notes, and error-code tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API documentation can omit details or infer descriptions when source inputs are incomplete.

Mitigation: Review generated endpoint descriptions, parameter tables, authentication notes, rate limits, and error-code guidance before publishing.

Risk: The included validation script contacts an external backend that may process documentation content.

Mitigation: Do not send confidential internal specs, endpoint details, or unreleased API documentation to the validation backend unless that processing is acceptable.

Risk: The skill is in maintenance mode and will not receive feature updates.

Mitigation: Use it for existing Chinese API documentation workflows, and consider the referenced alternative ClawHub skills for compliance-specific checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/cn-api-doc-writer)
- [Validation API base URL](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with JSON examples and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs Chinese API documentation using consistent terminology, realistic example values, request and response sections, error-code tables, and notes for fields needing manual review.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
