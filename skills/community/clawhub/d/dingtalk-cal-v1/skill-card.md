## Description: <br>
Helps agents manage DingTalk calendars by creating, querying, updating, and deleting events; checking availability; and finding or booking meeting rooms through mcporter-connected DingTalk MCP services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agent users use this skill to coordinate DingTalk schedules, check participant availability, search contacts, and reserve meeting rooms from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read coworker availability and contact data and can change, delete, or book calendar resources. <br>
Mitigation: Use an account with the least necessary DingTalk permissions and require explicit preview and confirmation before reading others' availability or modifying calendar resources. <br>
Risk: The configured mcporter package and DingTalk MCP URLs determine which external services the agent connects to. <br>
Mitigation: Verify the mcporter package and copy DingTalk MCP URLs from the official DingTalk MCP marketplace before configuration. <br>


## Reference(s): <br>
- [DingTalk MCP Marketplace](https://mcp.dingtalk.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/dingtalk-cal-v1) <br>
- [Publisher Profile](https://clawhub.ai/user/onlyloveher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON argument examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for mcporter CLI calls to DingTalk calendar and contacts MCP services.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence, released 2026-03-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
