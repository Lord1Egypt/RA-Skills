## Description: <br>
Manage ClickUp tasks, docs, time tracking, comments, chat, and search via official MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pvoo](https://clawhub.ai/user/pvoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to ClickUp through the official MCP server for workspace search, task updates, comments, docs, chat, and time tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses CLICKUP_TOKEN and the evidence describes the token as long-lived. <br>
Mitigation: Treat CLICKUP_TOKEN like a password, keep the environment file private, and replace the token if exposure is suspected. <br>
Risk: The skill gives the agent broad ClickUp workspace write and messaging abilities. <br>
Mitigation: Use the least-privileged ClickUp account or workspace available and require explicit confirmation before task, doc, time, comment, attachment, or chat changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pvoo/clickup-mcp) <br>
- [ClickUp](https://clickup.com) <br>
- [ClickUp MCP Documentation](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) <br>
- [ClickUp MCP Supported Tools](https://developer.clickup.com/docs/mcp-tools) <br>
- [ClickUp API Reference](https://clickup.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance can lead the agent to read or write ClickUp workspace content through MCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
