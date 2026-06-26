## Description: <br>
An agent-first CRM, built for an AI agent to operate over a plain-text HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pdparchitect](https://clawhub.ai/user/pdparchitect) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use CRM Kit to manage CRM contacts, companies, deals, activities, workspaces, members, tokens, reminders, and audit records through a headless HTTP API or MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses bearer-token access to CRM data, so exposed tokens could allow unauthorized access or modification. <br>
Mitigation: Treat bearer tokens like passwords, avoid exposing them in chat logs or screenshots, review active tokens periodically, and revoke unused sessions. <br>
Risk: The skill can create, update, or delete CRM and workspace records, including sensitive workspace actions. <br>
Mitigation: Confirm destructive or privileged actions with the user and use the documented confirmation or step-up flows before proceeding. <br>


## Reference(s): <br>
- [CRM Kit ClawHub Release](https://clawhub.ai/pdparchitect/crmkit) <br>
- [CRM Kit API](https://api.crmkit.ai) <br>
- [CRM Kit MCP Endpoint](https://api.crmkit.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown operating manual with HTTP endpoint descriptions, request conventions, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API responses are plain text by default and JSON when requested with an Accept header or format parameter.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
