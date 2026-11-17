## Description:

Redact personally identifiable information from text by replacing sensitive data with configurable placeholders using Expanso Edge pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to redact names, emails, phone numbers, identifiers, addresses, and other PII from text before storage, analytics, sharing, or public release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive text may be exposed through an unauthenticated network endpoint.

Mitigation: Run only on trusted hosts, avoid exposing the MCP server to a network, and add authentication and rate limits before broader deployment.

Risk: OpenAI processing can transfer PII off-device.

Mitigation: Treat remote model processing as an off-device data transfer and confirm the data handling requirements for regulated or confidential inputs.

Risk: Model output may be returned as redacted text without independent proof that all PII was removed.

Mitigation: Validate redaction results before relying on them and use a fail-closed error path for parsing or model-output failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-pii-redact)
- [ClawHub publisher profile](https://clawhub.ai/user/aronchick)
- [Expanso](https://expanso.io)
- [Expanso pii-redact pipeline](https://skills.expanso.io/pii-redact/pipeline-cli.yaml)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing redacted_text, redaction_count, redacted_types, and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The replacement placeholder is configurable; output includes trace metadata such as mode, model, placeholder, input hash, input length, trace ID, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
