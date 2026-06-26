## Description: <br>
Use this skill when you need to control or make actions on the user's Chrome tab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NmadeleiDev](https://clawhub.ai/user/NmadeleiDev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent-operated CLI to a live Chrome tab for browser observation, navigation, clicking, typing, key presses, scrolling, and troubleshooting bridge connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to control a live Chrome tab and grants broad browser authority with limited scoping and cleanup guidance. <br>
Mitigation: Install only when live browser control is intended; use a separate Chrome profile or test account, confirm sensitive actions before execution, and stop the bridge and disconnect the extension when finished. <br>
Risk: Operator and shared tokens can authorize bridge access if exposed or reused. <br>
Mitigation: Generate fresh strong tokens per session, keep the operator token private, pass it only through trusted channels, and use TLS for non-local deployments. <br>
Risk: The skill depends on an external CLI and Chrome extension outside the artifact bundle. <br>
Mitigation: Review the external CLI and extension source, pin trusted versions where possible, and install only versions that match the intended release. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/NmadeleiDev/browser-agent-bridge-cli) <br>
- [Browser Agent Bridge project link from skill artifact](https://github.com/NmadeleiDev/browser_agent_bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide an agent through installing and operating a browser bridge CLI; browser actions affect the connected live Chrome tab.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
