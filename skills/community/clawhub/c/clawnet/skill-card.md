## Description: <br>
P2P bot discovery for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dendisuhubdy](https://clawhub.ai/user/dendisuhubdy) <br>

### License/Terms of Use: <br>
MIT OR Apache-2.0 <br>


## Use Case: <br>
Developers and agent operators use ClawNet to let OpenClaw agents discover peers, announce presence, maintain peer and friend records, and communicate over a QUIC-based P2P network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad peer-to-peer networking, IP-range scanning, and identity-announcement behavior. <br>
Mitigation: Install only when internet-facing P2P discovery and messaging are intended, and avoid daemon or scan commands on sensitive networks. <br>
Risk: Scan commands can probe network ranges and may affect networks the operator does not control. <br>
Mitigation: Scan only authorized ranges and keep scans scoped to the smallest practical CIDR. <br>
Risk: Bot names, capabilities, metadata, and direct messages may disclose sensitive information to peers or beacon registries. <br>
Mitigation: Do not put secrets or sensitive operational details in identity, metadata, capability, announcement, or message fields. <br>
Risk: Beacon registration sends bot identity and capability data to a configured HTTP endpoint. <br>
Mitigation: Use only trusted HTTPS beacon registries. <br>


## Reference(s): <br>
- [ClawNet ClawHub page](https://clawhub.ai/dendisuhubdy/clawnet) <br>
- [Iroh](https://iroh.computer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [CLI text and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Most non-interactive commands support --json; chat is interactive.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
