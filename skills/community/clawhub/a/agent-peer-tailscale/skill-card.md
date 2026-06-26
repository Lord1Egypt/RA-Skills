## Description: <br>
Connects two OpenClaw agents on different machines as peer collaborators over Tailscale VPN for direct sessions_send communication without public IPs, port forwarding, or a middle server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect trusted OpenClaw agents on separate machines so they can exchange session context, review requests, tips, and task delegations over a private Tailscale network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Binding an OpenClaw gateway to 0.0.0.0 can expose it beyond the intended Tailscale interface. <br>
Mitigation: Prefer binding the gateway to the Tailscale IP, enforce Tailscale ACLs, and allow inbound gateway traffic only from trusted peers. <br>
Risk: Gateway tokens and generated peer configuration files may expose agent access if stored or shared insecurely. <br>
Mitigation: Keep tokens out of repositories and synced folders, restrict file permissions on generated configs, share tokens through a secure channel, and rotate tokens after setup. <br>
Risk: A trusted peer with gateway access can send messages that act through the receiving agent. <br>
Mitigation: Share access only with trusted peers, restrict target sessions where supported, and review peer messages before acting on sensitive tasks. <br>
Risk: Broad troubleshooting steps such as disabling firewall protections or generic file sharing can increase exposure. <br>
Mitigation: Use those steps only for isolated testing, re-enable protections immediately, and prefer narrow firewall rules for the Tailscale network. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/agent-peer-tailscale) <br>
- [Tailscale Setup](references/tailscale-setup.md) <br>
- [Peer Communication](references/peer-communication.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Tailscale download for Windows](https://tailscale.com/download/windows) <br>
- [Tailscale admin console](https://login.tailscale.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and peer configuration content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an interactive Python helper that can generate a peer-agent/peer-config.md file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
