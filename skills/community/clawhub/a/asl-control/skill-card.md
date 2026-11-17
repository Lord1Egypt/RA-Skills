## Description:

Monitor and control AllStar Link amateur radio nodes via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kj5irq](https://clawhub.ai/user/kj5irq)

### License/Terms of Use:


## Use Case:

External operators and developers use this skill to monitor an AllStar Link node, inspect connected nodes and audit logs, manage favorites, and issue connect, disconnect, and timed net-session commands through an ASL Agent REST API backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue live connect, disconnect, net start, net stop, and cron-driven net tick actions against an AllStar Link node.

Mitigation: Install it only for an ASL Agent backend you control, and require explicit user confirmation before commands that change live radio-node connections.

Risk: The client may send ASL_API_KEY over HTTP when pointed at an ordinary LAN or Internet endpoint.

Mitigation: Use HTTPS or a trusted encrypted tunnel such as Tailscale, avoid untrusted HTTP networks, and keep the API key least-privileged.

Risk: Timed net sessions and cron-based net tick can automatically disconnect a node after the configured duration.

Mitigation: Review net profile names, node numbers, and durations before starting a session, and log scheduled net tick output for operator review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kj5irq/skills/asl-control)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; invoked tooling returns JSON or concise text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus ASL_PI_IP and ASL_API_KEY environment variables; optional ASL_API_BASE and ASL_STATE_DIR change backend URL and local state storage.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
