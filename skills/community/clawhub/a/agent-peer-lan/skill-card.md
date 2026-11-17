## Description:

Connects two OpenClaw agents on the same trusted LAN as peer collaborators for direct sessions_send communication without a VPN, internet port forwarding, or third-party relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypnotronic3](https://clawhub.ai/user/hypnotronic3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure two OpenClaw agents on trusted LAN machines to exchange messages, delegate tasks, and troubleshoot peer connectivity without using a VPN or relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose an agent-control gateway on the local network.

Mitigation: Use it only on a trusted, isolated LAN; bind the gateway to a specific LAN IP when possible and restrict firewall rules to exact peer IPs.

Risk: Gateway tokens or sensitive task content may be sent over plain HTTP.

Mitigation: Require gateway authentication, avoid storing tokens in configuration files, and use TLS or an encrypted tunnel before sending tokens or sensitive tasks.

Risk: The artifact includes sudo/admin firewall commands that modify host network access.

Mitigation: Review commands before execution and apply only rules that match the trusted subnet or exact peer addresses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hypnotronic3/skills/agent-peer-lan)
- [Network Setup - LAN Peer Agent](references/network-setup.md)
- [Troubleshooting - LAN Peer Agent](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include LAN IPs, gateway URLs, firewall rules, and peer-agent/peer-config.md content; gateway tokens should not be stored in generated configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
