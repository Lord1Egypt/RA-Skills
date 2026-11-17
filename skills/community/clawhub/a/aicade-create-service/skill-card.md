## Description:

Use when preparing signed AICADE gateway service-management requests for service registration, service detail queries, or service disable operations, especially when collecting service metadata, auth config, billing, rate limits, JSON Schemas, serviceId, or signed curl output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aicadegalaxy](https://clawhub.ai/user/aicadegalaxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect AICADE gateway service-management inputs, validate service registration details, and generate signed curl commands for registration, detail lookup, or disable operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse local AICADE_API_KEY and AICADE_API_SECRET_KEY values and print authenticated curl commands.

Mitigation: Review generated commands before sharing or running them, prefer redacted or environment-variable-based output, and avoid putting real API keys or secrets in chat transcripts or logs.

Risk: Generated disable commands can affect an existing service when the base URL or serviceId is wrong.

Mitigation: Confirm the base URL and serviceId before generating or executing disable operations.

## Reference(s):

- [Service Management API Reference](references/service-management-api.md)
- [Register Service Guided Intake](references/register-intake.md)
- [Service Operations Guided Intake](references/service-operations-intake.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON snippets and signed curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands may include authentication headers; the bundled script prints requests and does not call the remote API.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
