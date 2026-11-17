## Description:

Detects personally identifiable information in text using Expanso Edge pipelines for CLI, MCP server, or cloud deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scan text, logs, support tickets, and pipeline payloads for PII before processing, logging, storing, or sharing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive text may be sent to OpenAI during PII detection.

Mitigation: Use only under the installer's own data-handling rules and avoid regulated, customer, employee, payment, health, or identity data unless that transfer is approved.

Risk: The advertised local regex mode is not available in this artifact.

Mitigation: Treat OpenAI-backed detection as the available operating mode and do not rely on this release for local-only PII scanning.

Risk: HTTP mode listens on all interfaces without authentication.

Mitigation: Bind MCP mode to localhost or a private interface, add authentication and rate limits, and avoid direct network exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-pii-detect)
- [Expanso Edge](https://expanso.io)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON object with findings, has_pii, summary, and metadata fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected PII values, positions, confidence scores, input metadata, and trace identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
