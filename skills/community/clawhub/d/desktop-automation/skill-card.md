## Description: <br>
Control the desktop via CUA computer server API running on port 8000. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarinali](https://clawhub.ai/user/sarinali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a local CUA computer server for screenshots, mouse and keyboard actions, window control, and desktop workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad live-screen desktop control and may be configured as an always-on service. <br>
Mitigation: Run the CUA server only while needed, keep it bound to localhost, close sensitive windows before use, and avoid always-on service mode unless the operator understands how to disable it. <br>
Risk: Network exposure of the CUA server can allow remote desktop control if access is not constrained. <br>
Mitigation: Use authentication for any network exposure, keep firewall rules restrictive, and prefer local-only access. <br>


## Reference(s): <br>
- [Desktop Automation on ClawHub](https://clawhub.ai/sarinali/desktop-automation) <br>
- [CUA Computer Server GitHub Repository](https://github.com/trycua/cua-computer-server) <br>
- [CUA Getting Started Documentation](https://cua.ai/docs/cua/guide/get-started/what-is-cua) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a CUA server on localhost:8000 by default and may control the live desktop.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
