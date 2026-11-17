## Description:

Automates FortiGate firewall configuration, including policy and address management plus industrial protocol security configuration for Modbus, IEC104, S7, and related ICS protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiansiting](https://clawhub.ai/user/jiansiting)

### License/Terms of Use:

MIT-0

## Use Case:

Network and security engineers use this skill to inspect and automate FortiGate firewall objects, policies, IPS profiles, industrial protocol service objects, and selected Industrial Connectivity settings through the FortiGate REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live changes to FortiGate firewall policies, address objects, services, IPS profiles, and interface access settings.

Mitigation: Use a least-privilege FortiGate API token, review requested changes before execution, and test outside production before use on live devices.

Risk: SSL verification defaults to false, which can expose administrative API traffic to interception when left unchanged.

Mitigation: Set FORTIGATE_VERIFY_SSL=true and use a valid certificate for the target FortiGate device.

Risk: Firewall policy automation can unintentionally broaden network access if inputs use overly broad source, destination, service, or action values.

Mitigation: Require explicit narrow policy inputs, review generated policy parameters, and keep rollback steps available before applying changes.

Risk: The configure-icond action changes interface access settings and may rely on FortiOS API behavior that needs environment-specific validation.

Mitigation: Avoid configure-icond until interface access impact, rollback behavior, and exact FortiOS API support are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiansiting/skills/fortigate-config)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text tables and status messages, with CLI command snippets for manual icond fallback.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses tabulate for grid-style policy tables when installed; otherwise falls back to aligned text.]

## Skill Version(s):

2.0.0 (source: artifact frontmatter; target metadata version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
