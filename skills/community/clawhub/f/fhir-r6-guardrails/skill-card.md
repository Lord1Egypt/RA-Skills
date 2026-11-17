## Description:

HealthClaw Guardrails provides FHIR agent guardrails for clinical data access through MCP, with support for FHIR R4 US Core v9 and experimental FHIR R6 ballot3 workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aks129](https://clawhub.ai/user/aks129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare AI teams use this skill to route FHIR read, search, write, audit, statistics, and access-control operations through MCP guardrails. It is intended for workflows that need PHI redaction, two-phase write review, step-up authorization, tenant isolation, and audit records around clinical data access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles clinical data and upstream FHIR queries, including query parameters that could contain PHI.

Mitigation: Confirm where upstream queries are sent, how PHI in parameters is handled, and whether deployment logging and retention policies match the intended clinical environment before installation.

Risk: The artifact claims immutability, compliance protections, and audit guarantees that may depend on deployment details outside the inspected skill text.

Mitigation: Verify audit storage, tamper-evidence, tenant isolation, and step-up authorization controls in the actual deployment instead of relying on the skill description alone.

## Reference(s):

- [HealthClaw](https://healthclaw.io)
- [ClawHub skill page](https://clawhub.ai/aks129/skills/fhir-r6-guardrails)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with inline tool names, configuration values, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tool outputs may include redacted FHIR resources, validation results, permission decisions, statistics, and audit-oriented status information.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
