## Description: <br>
配置和管理 OpenClaw-CN 浏览器模式（openclaw/chrome），解决浏览器连接问题. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yishanjiu-3386](https://clawhub.ai/user/Yishanjiu-3386) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw-CN users use this skill to configure browser mode, switch between OpenClaw-managed and Chrome relay profiles, and troubleshoot browser connectivity issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying examples can change local OpenClaw-CN browser configuration. <br>
Mitigation: Confirm the intended browser profile before editing settings and back up openclaw.json when needed. <br>
Risk: Chrome mode can use existing browser login sessions. <br>
Mitigation: Use Chrome mode only when sharing the current Chrome account state is intended; otherwise prefer the OpenClaw-managed browser profile. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Yishanjiu-3386/browser-config) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/Yishanjiu-3386) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes OpenClaw-CN is installed and available as openclaw-cn.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
