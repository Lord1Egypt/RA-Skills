## Description: <br>
Dingtalk Calendar helps agents guide DingTalk calendar creation, schedule lookup, coworker availability checks, and meeting room booking through mcporter-connected DingTalk MCP services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JavaZhengwu](https://clawhub.ai/user/JavaZhengwu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workspace operators use this skill to configure mcporter access to DingTalk calendar and contacts MCP services, then create, query, update, delete, and book calendar events and meeting rooms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured DingTalk MCP services can expose coworker availability and contact details. <br>
Mitigation: Query coworker busy status or contact details only when authorized, and prefer a least-privileged DingTalk account. <br>
Risk: Calendar update and delete operations can modify or remove DingTalk events. <br>
Mitigation: Confirm event IDs and intended changes before executing update or delete commands. <br>
Risk: The skill depends on the mcporter package and user-configured DingTalk MCP URLs. <br>
Mitigation: Install only if the mcporter package is trusted and verify DingTalk MCP URLs before configuration. <br>


## Reference(s): <br>
- [DingTalk MCP Plaza](https://mcp.dingtalk.com) <br>
- [ClawHub skill page](https://clawhub.ai/JavaZhengwu/dingtalk-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use mcporter to call configured DingTalk calendar and contacts MCP services.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact package.json and CHANGELOG show 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
