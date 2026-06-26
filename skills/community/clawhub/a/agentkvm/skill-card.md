## Description: <br>
Control physical devices such as phones, PCs, and Macs through NanoKVM-USB hardware by taking screenshots and sending mouse, keyboard, scroll, and drag actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamtwz](https://clawhub.ai/user/iamtwz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent observe and operate a connected physical device for GUI workflows, remote testing, and computer-use loops. The agent repeatedly screenshots the device, analyzes the visible UI, acts with input commands, and verifies the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent screen-viewing and input-control access to a connected physical device. <br>
Mitigation: Install and use it only when that level of device access is intended, supervise sensitive sessions, and avoid passwords, MFA codes, payments, deletions, or account changes unless directly monitored. <br>
Risk: Remote server mode can expose device control over a network if configured broadly or with weak access controls. <br>
Mitigation: Bind server mode to localhost or a trusted interface, require a strong token, protect access with a firewall or VPN, and stop the server when finished. <br>
Risk: The workflow depends on an external AgentKVM npm package, CLI tools, ffmpeg, and NanoKVM-USB hardware. <br>
Mitigation: Review the external package and local installation before trusting it, then verify each action with fresh screenshots before continuing automation. <br>


## Reference(s): <br>
- [AgentKVM API Reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/iamtwz/agentkvm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces action plans and commands for a separately installed AgentKVM CLI and connected NanoKVM-USB hardware.] <br>

## Skill Version(s): <br>
0.2.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
