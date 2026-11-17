## Description:

Streams Claude Code terminal output to a browser-based xterm.js viewer over WebSocket and provides APIs for process status, command sending, and restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1zn](https://clawhub.ai/user/1zn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor a local Claude Code session from another browser or device, embed terminal output in a dashboard, and send or restart commands through the provided HTTP and WebSocket interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes Claude Code terminal output and command control through a network-accessible service without authentication.

Mitigation: Run it only on a trusted, isolated machine; keep access localhost-only or behind authenticated controls; and do not expose the port to a LAN, VPN, or the public internet.

Risk: The launched Claude Code process is configured to skip permission checks.

Mitigation: Remove the permission-bypass flag or add explicit permission controls before using the skill with sensitive workspaces or credentials.

Risk: Terminal output may reveal sensitive data to anyone who can reach the viewer.

Mitigation: Treat displayed terminal output as sensitive and restrict viewer access to trusted users and networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1zn/skills/cc-log-viewer)
- [Project homepage](https://github.com/openclaw/cc-log-viewer)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local web service setup, browser access URLs, and HTTP API usage guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
