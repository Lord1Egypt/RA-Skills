## Description:

Connects an AI agent to real FHIR servers through an MCP guardrail proxy with URL rewriting, redaction, audit trails, and step-up authentication for upstream data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aks129](https://clawhub.ai/user/aks129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare integration engineers use this skill to configure an AI agent path to HAPI FHIR, SMART Health IT, Epic sandbox, or production EHR FHIR servers while keeping proxy guardrails active.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FHIR query parameters, upstream responses, and audit logs may contain identifiers or PHI.

Mitigation: Confirm the upstream server, auth model, audit retention, and compliance expectations before installation; use minimum-necessary search parameters and treat query strings and logs as sensitive.

Risk: The skill notes no SMART-on-FHIR auth forwarding and no upstream tenant isolation, so upstream authorization and tenant controls are outside the local proxy boundary.

Mitigation: Verify the upstream server's native authorization and tenant controls before using the proxy with production clinical data.

Risk: No caching means every proxied request reaches the upstream FHIR server.

Mitigation: Plan for upstream availability, rate limits, and monitoring before connecting agents to production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aks129/skills/fhir-upstream-proxy)
- [HAPI FHIR R4 test server](https://hapi.fhir.org/baseR4)
- [SMART Health IT R4 server](https://r4.smarthealthit.org)
- [HAPI FHIR R5 test server](https://hapi.fhir.org/baseR5)
- [Epic FHIR sandbox](https://open.epic.com/Interface/FHIR)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable settings, tested upstream server examples, behavior notes, and limitations.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
