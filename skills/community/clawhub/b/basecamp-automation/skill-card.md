## Description: <br>
Automate Basecamp project management, to-dos, messages, people, and to-do list organization via Rube MCP (Composio). Always search tools first for current schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to manage Basecamp projects, to-do lists, tasks, messages, people, and access through Rube MCP. It is intended for workflows where the connected Basecamp account, target project, message content, recipients, assignees, and access changes can be confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real project, task, message, people, and membership changes through a connected Basecamp account. <br>
Mitigation: Install only if the Rube MCP provider and connected Basecamp account are trusted, and confirm target projects, message content, assignees, recipients, and access changes before running write actions. <br>
Risk: Using outdated or mismatched tool schemas can send requests with incorrect parameters or route changes to the wrong Basecamp object. <br>
Mitigation: Search Rube tools for current schemas before workflows and resolve IDs top-down from projects to to-do sets, message boards, lists, tasks, and people. <br>


## Reference(s): <br>
- [Rube MCP](https://rube.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with tool names, ordered workflow steps, parameters, and cautions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Rube MCP and an active Basecamp connection; rich text content should use HTML rather than Markdown.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
