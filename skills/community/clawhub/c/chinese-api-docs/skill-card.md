## Description:

Generates professional Chinese API documentation from code, OpenAPI or Swagger specs, or endpoint descriptions, with terminology guidance, examples, error-code tables, authentication notes, rate-limit sections, and optional validation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to create Chinese-language REST API reference documentation from OpenAPI or Swagger specs, code, or endpoint descriptions. It helps standardize Chinese technical terminology, request and response examples, authentication guidance, rate-limit notes, and error-code documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External validation may send API documentation or specifications to a third-party service without clear data-handling documentation.

Mitigation: Avoid using validation with private API specs, unreleased endpoints, secrets, customer data, or proprietary schemas unless the publisher documents what is sent and explicit consent is obtained.

Risk: The security verdict is suspicious because validation data-flow behavior is not clearly explained.

Mitigation: Review the validation script before use and disable or avoid network validation in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/chinese-api-docs)
- [Validation API base URL](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown API documentation with JSON and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use an external validation endpoint when the bundled validation script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
