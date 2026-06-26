## Description: <br>
Composio helps an agent discover tools, manage third-party app connections, execute actions across connected services, and process larger workflows through remote workbench tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjayesh](https://clawhub.ai/user/wjayesh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to connect AI agents to Composio-supported apps, find the right tools for a task, manage required account connections, execute actions, and process large tool outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected app actions can send, post, edit, delete, upload, or otherwise change data in third-party accounts. <br>
Mitigation: Use a dedicated Composio project, connect only required accounts, review OAuth scopes, and require explicit user confirmation before state-changing actions. <br>
Risk: The remote workbench and bash tools can run persistent remote code and process large outputs outside the local agent session. <br>
Mitigation: Use remote execution only for necessary processing, keep code scoped to the task, avoid secrets in code or logs, and revoke connections after the task is complete. <br>
Risk: The Composio API key grants access to connected Composio capabilities if exposed. <br>
Mitigation: Store the API key in a private environment variable, do not paste it into shared output, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/wjayesh/composio) <br>
- [Composio platform](https://platform.composio.dev) <br>
- [Composio API base](https://backend.composio.dev/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown instructions with JSON payload examples, cURL commands, and Python or Bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authentication URLs, tool execution responses, remote workbench output, and uploaded artifact links through Composio services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
