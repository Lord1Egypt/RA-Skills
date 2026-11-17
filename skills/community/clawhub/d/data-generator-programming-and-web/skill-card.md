## Description:

Generates development and test data such as UUIDs, random strings, numbers, colors, emails, IP addresses, Lorem Ipsum, timestamps, passwords, API keys, and JWT secrets through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate disposable development, testing, and prototyping data, including identifiers, placeholder content, timestamps, and credential-like random strings. It is intended for AgentPMT-hosted remote tool calls rather than local command execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords, API keys, or JWT signing secrets may be mistaken for production-ready credentials even though the security evidence recommends disposable development use only.

Mitigation: Use generated secrets only for disposable development data unless the generator, transport, storage, and credential-handling policies have been independently reviewed.

Risk: The skill depends on mutable remote instructions and AgentPMT-hosted tool behavior.

Mitigation: Review live schema and instructions before production integration, and verify setup skills and versions before sending credentials or payment-related data.

## Reference(s):

- [Data Generator schema](artifact/schema.md)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/data-generator-programming-and-web)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/data-generator-programming-and-web)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON call examples and generated text or JSON values returned by remote tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The product-specific actions return generated values for development and testing workflows; security-sensitive values should be treated as disposable unless independently reviewed.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
