## Description: <br>
Persistent project planning for AI agents. Create, manage, and track long-term goals using structured Kanban boards that survive session resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akievo](https://clawhub.ai/user/akievo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Akievo to give an OpenClaw agent persistent, human-editable Kanban planning for long-running goals, task tracking, dependencies, and progress reporting across session resets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify persistent project boards in the connected Akievo account. <br>
Mitigation: Install only when that behavior is desired, use the narrowest available API key scopes, and require confirmation before creating or deleting durable records. <br>
Risk: Board text, comments, and attachments may persist sensitive information. <br>
Mitigation: Avoid storing secrets or regulated data in Akievo content, and revoke the API key when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/akievo/akievo) <br>
- [Akievo Setup Guide](https://akievo.com/openclaw-setup) <br>
- [Akievo API Documentation](https://akievo.com/api-docs) <br>
- [Akievo MCP Endpoint](https://mcp.akievo.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with MCP tool calls and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AKIEVO_API_KEY and can create, update, block, complete, and comment on persistent Akievo boards.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
