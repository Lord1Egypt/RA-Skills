## Description:

Connects two OpenClaw agents on different machines as peer collaborators over Tailscale VPN for direct sessions_send communication without public IPs, port forwarding, or a middle server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure two OpenClaw gateways so agents on separate machines can exchange session context, status updates, review requests, and delegated work over a private Tailscale network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway listeners may be exposed more broadly than intended when configured to bind to 0.0.0.0.

Mitigation: Bind OpenClaw to the Tailscale IP where possible and restrict inbound firewall rules to the Tailscale network.

Risk: Gateway tokens may be stored in plaintext peer configuration files.

Mitigation: Avoid storing tokens in peer-config.md; use a password manager, local secrets store, or environment-specific secure storage.

Risk: Reusable or long-lived Tailscale auth keys can allow unwanted peers to join the private network.

Mitigation: Use one-time short-lived auth keys and revoke keys from the Tailscale admin console when access is no longer needed.

Risk: Installer commands fetched directly with curl can run unreviewed code.

Mitigation: Prefer platform package managers or independently verify installer contents before execution.

Risk: A trusted peer can send messages that influence or execute through the receiving agent.

Mitigation: Share access only with trusted peers, require strong gateway authentication, and limit which sessions peers can target.

## Reference(s):

- [Peer Communication - Message Formats and Collaboration Patterns](references/peer-communication.md)
- [Tailscale Setup - Detailed Guide](references/tailscale-setup.md)
- [Troubleshooting - Connection Problems](references/troubleshooting.md)
- [Tailscale Linux Install Script](https://tailscale.com/install.sh)
- [Tailscale Windows Download](https://tailscale.com/download/windows)
- [Tailscale Login](https://login.tailscale.com)
- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/skills/agent-peer-tailscale)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and an optional Python configuration generator]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces peer setup instructions, communication patterns, troubleshooting guidance, and local peer configuration files when the helper script is run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
