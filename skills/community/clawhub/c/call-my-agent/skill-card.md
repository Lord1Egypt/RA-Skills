## Description: <br>
Create a private internet voice line between a user and an OpenClaw agent without Twilio or phone number rental, using local OpenClaw auth and Tailscale private access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrbese](https://clawhub.ai/user/mrbese) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up a local private voice interface for an OpenClaw agent, configure authentication and remote access, and verify the privacy boundary before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation, dependency setup, remote access, and background service steps can change the user's machine. <br>
Mitigation: Require explicit user confirmation before package installation, npm install, Tailscale Serve changes, persistence setup, or starting a long-running service. <br>
Risk: OpenAI API keys or other sensitive credentials could be exposed if pasted into chat or stored outside the intended auth flow. <br>
Mitigation: Use existing OpenClaw auth profiles first and keep OpenAI keys inside OpenClaw auth rather than pasting them into chat. <br>
Risk: Binding the local voice app beyond localhost can expose it on a LAN or public network. <br>
Mitigation: Use the default 127.0.0.1 binding unless the user intentionally confirms broader exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrbese/call-my-agent) <br>
- [Publisher profile](https://clawhub.ai/user/mrbese) <br>
- [Public app repository listed in artifact](https://github.com/mrbese/call-my-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup, service management, Tailscale access, teardown, verification, and privacy-check guidance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
