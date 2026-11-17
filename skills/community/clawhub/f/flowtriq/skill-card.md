## Description:

Monitor and manage Flowtriq DDoS detection in real time using the Flowtriq API for active attacks, node status, incident history, traffic metrics, PCAP captures, configuration, and mitigation status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacob-masse](https://clawhub.ai/user/jacob-masse)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operations teams use this skill to ask an agent for Flowtriq infrastructure monitoring, DDoS incident status, traffic context, node configuration, and response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Flowtriq access can expose incident data, traffic metrics, node configuration, and sensitive network metadata.

Mitigation: Configure credentials only for intended accounts and nodes, and review usage before installation when Flowtriq data includes customer traffic or regulated information.

Risk: Incident creation, incident updates, node registration, and PCAP uploads can change Flowtriq state or transmit sensitive packet data.

Mitigation: Require explicit user confirmation before registering nodes, opening or updating incidents, or uploading PCAP files.

## Reference(s):

- [Flowtriq API Endpoints Reference](references/api-endpoints.md)
- [Flowtriq Attack Types Reference](references/attack-types.md)
- [Flowtriq Platform](https://flowtriq.com)
- [Flowtriq Rate Limits Documentation](https://flowtriq.com/docs?section=rate-limits)
- [Flowtriq Status](https://flowtriq.com/status)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown with plain-language summaries, API request details, configuration guidance, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FLOWTRIQ_API_KEY and FLOWTRIQ_NODE_UUID for authenticated Flowtriq node operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
