## Description:

ClawNet enables OpenClaw bots to discover peers, announce presence, and communicate directly using a QUIC-based P2P network with NAT traversal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dendisuhubdy](https://clawhub.ai/user/dendisuhubdy)

### License/Terms of Use:

MIT OR Apache-2.0

## Use Case:

Developers and agent operators use ClawNet to let OpenClaw bots discover each other, announce capabilities, manage known peers, and exchange direct messages over a P2P network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a bot to internet-based P2P discovery and messaging traffic.

Mitigation: Install only when that exposure is intended, review firewall rules, and understand daemon-mode behavior before use.

Risk: Discovery and scanning behavior may touch networks the operator does not control.

Mitigation: Limit scanning and discovery activity to networks and peers where the operator has authorization.

Risk: Identity keys and local peer or friend stores are sensitive operational data.

Mitigation: Protect the identity key and local data files with appropriate filesystem permissions and secret-handling practices.

## Reference(s):

- [ClawNet Skill Page](https://clawhub.ai/dendisuhubdy/skills/clawnet)
- [iroh](https://iroh.computer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Command-line text and machine-readable JSON output, with local TOML and JSON configuration or data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive chat is text-stream oriented; most non-chat commands support --json output.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, Cargo.toml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
