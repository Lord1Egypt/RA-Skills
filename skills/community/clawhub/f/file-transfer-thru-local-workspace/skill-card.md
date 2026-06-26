## Description: <br>
Provides an OpenClaw web interface for uploading, downloading, listing, deleting, and packaging local workspace files and installed skill packages for agent-assisted file analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengwang86](https://clawhub.ai/user/chengwang86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to run a local browser-accessible file transfer service for moving files into the workspace, managing uploaded files, and downloading installed skill packages so an agent can inspect or process local materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent browser-accessible file manager on port 15170 with access to uploaded files and installed skill packages. <br>
Mitigation: Install only when that local service is intended, use a strong gateway token, and restrict network access to trusted hosts or localhost with firewall rules. <br>
Risk: Authentication can fall back to password-only or no-auth configurations, increasing exposure if the port is reachable by untrusted users. <br>
Mitigation: Avoid no-auth deployments, configure a gateway token, and do not expose the service on shared or public machines unless the workspace contents are acceptable to access through it. <br>
Risk: Generated service configuration may contain copied credentials in environment variables. <br>
Mitigation: Inspect generated systemd service environment after installation, remove stored credentials where possible, and rotate affected tokens if the service file was exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengwang86/file-transfer-thru-local-workspace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with URLs, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed service also creates and manages local uploaded files and skill package archives in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
3.1.1 (source: server release evidence, artifact metadata, package.json, SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
