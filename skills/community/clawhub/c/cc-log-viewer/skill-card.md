## Description: <br>
Cc Log Viewer streams Claude Code terminal output to a browser through WebSocket, supports remote or embedded monitoring, and provides Claude Code process management and command-sending controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1zn](https://clawhub.ai/user/1zn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local browser-based viewer for monitoring Claude Code sessions from the same machine, LAN, or private remote network and, when enabled, send commands or restart the session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local service exposes unauthenticated command sending and restart controls for the Claude Code session. <br>
Mitigation: Run it only in a tightly controlled local environment, add authentication before any shared access, and separate read-only log viewing from command and restart controls. <br>
Risk: The service listens on a network interface and may be reachable from LAN, Tailscale, or internet-routed environments. <br>
Mitigation: Bind the service to localhost or a trusted interface and do not expose it to broader networks unless access controls are added. <br>
Risk: The launched Claude Code process uses a permission-bypass flag. <br>
Mitigation: Remove the permission-bypass flag before normal use and review the process permissions for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1zn/cc-log-viewer) <br>
- [Project homepage](https://github.com/openclaw/cc-log-viewer) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, local service URLs, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes instructions for launching a local Node.js WebSocket/HTTP service and observing Claude Code terminal output in a browser.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
