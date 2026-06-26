## Description: <br>
Coze-Power bridges Coze cloud bots to local machine capabilities through a lightweight HTTP server and Coze-compatible OpenAPI plugin for web search, file operations, command execution, clipboard access, desktop notifications, and system information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homesickjava](https://clawhub.ai/user/homesickjava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Coze bot builders use this skill to expose selected local machine functions to Coze agents, including local file access, command execution, web search, clipboard operations, notifications, and system status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A public tunnel can expose local file writes, clipboard access, and shell command execution to a cloud-connected bot. <br>
Mitigation: Run the server only when this bridge is intentionally needed, change the API key before use, avoid public exposure unless necessary, and place the service in a container or VM when possible. <br>
Risk: Broad allowed_paths and allowed_commands settings can increase the impact of unintended tool calls. <br>
Mitigation: Narrow allowed_paths and allowed_commands to the minimum needed for each workflow and avoid granting access to sensitive directories or high-impact commands. <br>
Risk: Clipboard reads, clipboard writes, and file writes can expose or alter sensitive local data. <br>
Mitigation: Do not enable these workflows around sensitive data, confirm paths before reads or writes, and run the service on demand rather than continuously. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/homesickjava/coze-power) <br>
- [Coze-Power API Reference](references/api-reference.md) <br>
- [Coze Plugin Setup Guide](references/coze-plugin-setup.md) <br>
- [Coze-Power Examples](references/examples.md) <br>
- [OpenAPI Specification](assets/openapi-spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON/OpenAPI configuration and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent outputs may include API setup steps, command examples, file-operation guidance, and Coze plugin configuration details.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
