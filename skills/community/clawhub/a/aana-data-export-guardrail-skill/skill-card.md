## Description:

Checks export scope, destination, privacy, redaction, and approval before files, records, datasets, logs, or account data are exported or shared.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to gate data export requests by checking scope, destination, privacy sensitivity, redaction, approval, and retention before sharing files, records, datasets, logs, reports, messages, or account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad, bulk, cross-account, external, public, or sensitive exports can disclose private or regulated data when scope, recipient, retention, or approval is unclear.

Mitigation: Use the skill's checks to narrow scope, redact sensitive fields, verify destination and retention, require approval, or block unauthorized and excessive exports.

Risk: A configured checker could receive unnecessary sensitive details if review payloads include full records, secrets, logs, customer data, or unrelated private data.

Mitigation: Send only the minimal redacted review payload described by the skill and use the optional checker path only with a trusted, properly configured review service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-data-export-guardrail-skill)
- [Data export guardrail schema](artifact/schemas/data-export-guardrail.schema.json)
- [Redacted data export guardrail example](artifact/examples/redacted-data-export-guardrail.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with a structured text decision pattern and optional JSON-compatible review payload.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; may ask, redact, require approval, route to review, or block risky exports.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact manifest lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
