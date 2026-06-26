## Description: <br>
向日葵远程控制 provides an agent with tools for remote device management, remote session control, desktop interaction, screenshots, command execution, port forwarding, and remote power actions through the Awesun MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cutecube](https://clawhub.ai/user/cutecube) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage authorized Awesun remote devices, open and close remote sessions, inspect desktops, execute remote commands, configure port forwarding, and perform remote wake or shutdown operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad remote-control authority through generic MCP tool forwarding, including screenshots, remote commands, port forwarding, shutdown, reboot, and wake actions. <br>
Mitigation: Install only for systems the user owns or is authorized to administer, confirm the reachable MCP server and tools before use, and require explicit confirmation before high-impact remote-control actions. <br>
Risk: Misconfigured MCP server paths, API URLs, or tokens can connect the agent to an unintended remote-control endpoint. <br>
Mitigation: Review the MCP configuration before deployment and restrict the configuration to the intended local Awesun service and token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cutecube/awesun-remote-control) <br>
- [Awesun MCP service](https://github.com/OrayDev/awesun-mcp) <br>
- [Awesun UI locator](https://github.com/OrayDev/awesun-ui-locator) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, screenshots, guidance] <br>
**Output Format:** [Tool responses may include text, JSON-like data, command output, configuration snippets, session identifiers, and base64-encoded screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authorized local Awesun MCP server, Awesun API URL, and Awesun API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
