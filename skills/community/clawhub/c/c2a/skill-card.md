## Description: <br>
Manages 1Panel app-store workflows so an agent can search, inspect, install, uninstall, and list installed applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainsunsun](https://clawhub.ai/user/rainsunsun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and 1Panel administrators use this skill to manage app-store applications through natural-language requests. It supports searching the store, reviewing app details and versions, listing installed apps, and performing install or uninstall actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or uninstall 1Panel applications, including batch removals, without built-in confirmation or preview safeguards. <br>
Mitigation: Require explicit human confirmation in the agent workflow before install, uninstall, or batch uninstall actions. <br>
Risk: The skill requires a 1Panel API key and can administer the configured server. <br>
Mitigation: Use a least-privilege API key where possible and verify how the host stores saved credentials before use. <br>
Risk: Running the skill against production 1Panel systems could cause service changes or removals. <br>
Mitigation: Use it on production systems only when the workflow requires review and approval for changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/rainsunsun/c2a) <br>
- [Publisher profile](https://clawhub.ai/user/rainsunsun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger authenticated 1Panel API operations when the host agent executes the requested tool calls.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
