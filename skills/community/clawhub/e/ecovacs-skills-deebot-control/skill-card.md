## Description: <br>
Control Ecovacs Deebot vacuums via the IoT API and a gateway for device discovery, battery and status checks, cleaning, docking, and nickname-based robot selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ecovacs-ai](https://clawhub.ai/user/ecovacs-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and integrators use this skill to let an assistant operate Ecovacs Deebot robot vacuums through an Ecovacs Open Platform Access Key and compatible gateway. It supports listing robots, checking battery and work state, starting or pausing cleaning, sending a unit to charge, and interpreting common command failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An Ecovacs Open Platform Access Key can authorize vacuum control if exposed. <br>
Mitigation: Keep the AK private, avoid sharing it in chats or URLs, and store it only in trusted environment variables or local configuration. <br>
Risk: Cleaning or docking commands cause a physical robot to move. <br>
Mitigation: Confirm the target device, command, and surrounding area are safe before sending cleaning or docking actions. <br>
Risk: A wrong regional portal or untrusted gateway can cause failed commands or credential exposure. <br>
Mitigation: Use the official portal matching the account region or a trusted self-hosted gateway. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/ecovacs-ai/ecovacs-skills-deebot-control) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [Ecovacs Deebot Control API Reference](references/api.md) <br>
- [Internal Implementation Reference](references/agent-internal.md) <br>
- [Ecovacs Open Platform China](https://open.ecovacs.cn/) <br>
- [Ecovacs Open Platform Global](https://open.ecovacs.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, curl examples, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include robot-control commands that require a user-provided Ecovacs Open Platform Access Key and a regional or trusted self-hosted gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
