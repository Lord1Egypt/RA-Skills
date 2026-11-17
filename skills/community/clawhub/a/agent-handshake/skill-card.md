## Description:

Agent Handshake helps discover, register, and reconnect to AI agent servers by exchanging server identity records and supporting LAN, cloud, and Cloudflare Tunnel connection paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyliefeng](https://clawhub.ai/user/lyliefeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Agent Handshake to register and recognize AI agent servers, persist server identity, and run follow-up handshake or remote agent tasks across LAN, cloud, or NAT environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable HTTP-based remote command execution on agent servers.

Mitigation: Use it only when remote administration is intended, with least-privilege service accounts and audit logging.

Risk: Weak default or reused credentials could expose server control.

Mitigation: Replace defaults with unique high-entropy credentials and stronger authentication where available.

Risk: Public quick tunnels can expose command execution endpoints beyond the local network.

Mitigation: Avoid anonymous public tunnels for command execution; prefer HTTPS with controlled access and explicit exposure review.

Risk: Discovery and inventory behavior can reveal network or server details.

Mitigation: Define scan boundaries, protect stored server identity records, and review the complete script implementation before installation.

## Reference(s):

- [Server-resolved source repository](https://github.com/lyliefeng/agent-handshake)
- [ClawHub skill page](https://clawhub.ai/lyliefeng/skills/agent-handshake)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented identity records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include server connection details, identity metadata, and remote agent task results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
