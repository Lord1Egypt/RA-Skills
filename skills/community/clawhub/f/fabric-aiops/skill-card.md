## Description:

Operates network fabrics through controller APIs, providing inventory and health analysis plus governed configuration actions across Cisco Meraki, Catalyst Center, Cisco ACI, Arista CloudVision, and UniFi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

External network engineers and developers use the skill through an agent to inspect controller-managed networks, analyze device and network health, and perform supported remediation. It covers Meraki, Catalyst Center, Cisco ACI, Arista CloudVision, and UniFi, with platform-specific read and write coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because documented production-changing tools are available to an agent without an enforced approval gate.

Mitigation: Use read-only controller credentials for observation. Restrict write-capable credentials and require a person to review previews and approve changes.

Risk: The security scan is partial: three local references could not be resolved, and behavioral code analyzers were not applicable.

Mitigation: Treat the scan as incomplete, review the unresolved reference material, and assess the packaged behavior before using write-capable credentials.

## Reference(s):

- [Capabilities reference](artifact/references/capabilities.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [CLI reference](artifact/references/cli-reference.md)
- [ClawHub release](https://clawhub.ai/zw008/skills/fabric-aiops)
- [Publisher profile](https://clawhub.ai/user/zw008)
- [Project homepage listed in skill metadata](https://github.com/AIops-tools/Fabric-AIops)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Structured controller data with concise text analysis, plus command and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on platform support and controller responses; write operations can affect live network devices and configuration.]

## Skill Version(s):

0.15.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
