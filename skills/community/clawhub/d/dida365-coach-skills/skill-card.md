## Description: <br>
A task-coaching skill that combines Dida/TickTick MCP access with a local productivity system to break goals into plans, create time boxes, manage tasks, track commitments, run weekly and monthly reviews, and follow up on unfinished work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siyuanfeng636-cpu](https://clawhub.ai/user/siyuanfeng636-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to plan goals, schedule focused work, and manage Dida/TickTick tasks through natural-language coaching. It is also used to maintain a lightweight local productivity layer for commitments, focus records, dashboards, and review summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Dida/TickTick tasks through MCP-backed task actions. <br>
Mitigation: Install it only when task read/write access is acceptable, and review proposed task creation, update, move, completion, or batch actions before allowing them. <br>
Risk: Optional setup flows can modify local agent configuration files such as OpenClaw MCP settings. <br>
Mitigation: Confirm before allowing local configuration edits, and inspect the resulting MCP server entry if the environment or client is shared. <br>
Risk: The optional local Open API OAuth helper can store OAuth credentials in plaintext at ~/.dida-coach/dida-openapi.env. <br>
Mitigation: Prefer the normal MCP authorization path unless local OAuth is needed; if used, protect the file permissions and delete the file when no longer required. <br>
Risk: Broad automatic routing may select task-management behavior for varied natural-language requests. <br>
Mitigation: Use the skill's write-after-readback pattern and require explicit confirmation for high-risk or bulk task changes. <br>


## Reference(s): <br>
- [Dida Field Semantics](artifact/references/dida-field-semantics.md) <br>
- [MCP Client Setup](artifact/references/mcp-client-setup.md) <br>
- [MCP Tool Routing](artifact/references/mcp-tool-routing.md) <br>
- [OpenAPI Auth Setup](artifact/references/openapi-auth-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Natural-language coaching responses with Markdown, inline shell commands, configuration snippets, and MCP-backed task actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local productivity summaries and optional OAuth credential files when the user chooses those flows.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
