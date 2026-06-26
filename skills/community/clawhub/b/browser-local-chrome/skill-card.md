## Description: <br>
Configures and manages a local Google Chrome debug-mode browser for OpenClaw browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulike](https://clawhub.ai/user/liulike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to start, stop, troubleshoot, and configure a local Chrome instance for OpenClaw browser tasks such as JavaScript-rendered pages, screenshots, form interaction, and page analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful local Chrome control through CDP for browser automation. <br>
Mitigation: Use it only on trusted machines, keep the debug port bound to localhost, use a disposable Chrome profile, and close Chrome when automation is finished. <br>
Risk: The skill promotes private-network access and broad SSRF bypass behavior. <br>
Mitigation: Disable private-network access unless it is explicitly required, and prefer a narrow hostname allowlist for routine use. <br>
Risk: The setup flow can modify OpenClaw browser configuration and launch or stop local Chrome processes. <br>
Mitigation: Review the configuration change before use, back up existing OpenClaw settings, and run the skill in an isolated environment when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liulike/browser-local-chrome) <br>
- [README.md](README.md) <br>
- [INSTALL.md](INSTALL.md) <br>
- [HYBRID-MODE.md](HYBRID-MODE.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and configuration target local Chrome, localhost CDP, and OpenClaw browser settings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
