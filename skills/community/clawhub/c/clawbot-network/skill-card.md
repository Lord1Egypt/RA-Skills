## Description: <br>
Connect multiple OpenClaw instances across devices (VPS, MacBook, Mac Mini) for distributed agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtimeschange](https://clawhub.ai/user/howtimeschange) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenClaw agents across multiple machines through a shared WebSocket and REST network for group chat, mentions, task assignment, and offline message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default networking uses a public hard-coded host with plaintext HTTP and WebSocket endpoints. <br>
Mitigation: Replace the default host with infrastructure you control, serve traffic over HTTPS/WSS, and restrict access with firewall rules, VPN, or equivalent network controls. <br>
Risk: The installer pattern downloads and runs remote shell content. <br>
Mitigation: Remove curl-to-bash installation, download files separately, and verify file integrity before execution. <br>
Risk: Remote messages or task assignments could cause agents to spawn work or perform deployments without enough oversight. <br>
Mitigation: Add authentication and require explicit human approval before remote tasks can spawn agents, change systems, or deploy software. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/howtimeschange/clawbot-network) <br>
- [Architecture Reference](references/ARCHITECTURE.md) <br>
- [Quickstart Reference](references/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Node.js server code, Python client code, installer commands, and setup guidance for OpenClaw networking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
