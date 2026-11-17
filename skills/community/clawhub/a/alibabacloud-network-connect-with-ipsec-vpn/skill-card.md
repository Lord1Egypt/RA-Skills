## Description:

Guides agents through connecting Linux servers to an Alibaba Cloud VPC over dual-tunnel IPsec VPN using Aliyun CLI and StrongSwan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network engineers use this skill to collect parameters, create Alibaba Cloud VPN resources, configure StrongSwan on Linux, and verify dual-tunnel connectivity between a server network and a VPC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe SSH, credential, installation, and firewall guidance that should be reviewed before use.

Mitigation: Review and tighten operational steps before execution: remove StrictHostKeyChecking=no, verify CLI downloads, avoid exposing cloud secrets in flags or logs, and restrict firewall rules to confirmed VPN gateway peers.

Risk: The workflow creates paid cloud networking resources and changes Linux networking configuration.

Mitigation: Confirm all user-provided parameters and costs before creation, back up existing StrongSwan configuration, verify route and tunnel state after changes, and require explicit confirmation before cleanup or deletion commands.

Risk: Weak or exposed pre-shared keys can compromise the VPN connection.

Mitigation: Generate a unique strong PSK, avoid printing it in plain text, store it securely, and rotate it according to local security policy.

## Reference(s):

- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [RAM Policies](references/ram-policies.md)
- [Server-side Pre-check](references/server-precheck.md)
- [StrongSwan Configuration Reference](references/strongswan-config.md)
- [StrongSwan Quick Setup Guide (VICI/swanctl Method)](references/strongswan-config-templates/QUICKSTART.md)
- [Verification Method](references/verification-method.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Acceptance Criteria: alibabacloud-network-connect-using-ipsec](references/acceptance-criteria.md)
- [Related APIs and CLI Commands](references/related-apis.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guided parameter collection, confirmation checkpoints, cloud resource commands, StrongSwan configuration steps, verification steps, troubleshooting guidance, and optional cleanup commands.]

## Skill Version(s):

0.0.1-beta.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
