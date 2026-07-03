## Description: <br>
Dingtalk Meetings Skill helps agents manage DingTalk calendar meetings, including event creation, updates, cancellation, attendee management, availability checks, room booking, calendar permissions, and meeting invitations through DingTalk MCP servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpsean](https://clawhub.ai/user/cpsean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers with MCP-capable agents use this skill to schedule and manage DingTalk calendar meetings, inspect availability, invite attendees, and book rooms while confirming write actions before calling DingTalk tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DingTalk calendar access and optional contacts access can expose sensitive calendar, identity, and colleague information. <br>
Mitigation: Install only when this access is acceptable, enable the contacts MCP only when attendee lookup is needed, and avoid sharing the personal API URL. <br>
Risk: MCP setup and attendee lookup can create local configuration or cache files that contain access URLs or colleague identifiers. <br>
Mitigation: Review MCP configuration changes, keep API URLs out of version control, and periodically inspect or delete references/contacts.cache when identifiers should not be retained. <br>
Risk: Meeting creation, updates, deletion, permissions changes, and room booking modify cloud calendar state. <br>
Mitigation: Preview the full action details and require explicit user confirmation before write operations; use read-only listing tools first when the target event is ambiguous. <br>


## Reference(s): <br>
- [DingTalk Calendar MCP setup](https://aihub.dingtalk.com/#/detail?mcpId=1050&detailType=marketMcpDetail) <br>
- [DingTalk Contacts MCP setup](https://aihub.dingtalk.com/#/detail?mcpId=2400&detailType=marketMcpDetail) <br>
- [DingTalk developer getting started](https://open.dingtalk.com/document/dingstart/dingtalk-developer) <br>
- [DingTalk calendar and contacts MCP tool reference](references/mcp-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and MCP tool call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires dingtalk-calendar MCP access; dingtalk-contacts is optional for attendee lookup. Write actions should be previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
