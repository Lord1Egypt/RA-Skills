## Description: <br>
Communicate with a CoPaw instance through its HTTP API to inspect agents or chats, create chat sessions, send messages, and understand auth, scoping, and SSE behavior before integration work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erview](https://clawhub.ai/user/erview) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate with a CoPaw instance through its HTTP API, especially for chat/session creation, agent-scoped console messaging, and SSE response handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the guidance against a live CoPaw instance may expose credentials or chat contents if the target host and authentication scope are not confirmed. <br>
Mitigation: Confirm the intended CoPaw host, use least-privilege credentials, and avoid sending unnecessary secrets into chat sessions. <br>
Risk: Workspace import/export, MCP configuration, cron, skills, tools, and file-management endpoints can affect administrative state or expose workspace contents. <br>
Mitigation: Require explicit user intent before using administrative endpoints and review the requested operation before execution. <br>


## Reference(s): <br>
- [CoPaw API Chat release page](https://clawhub.ai/erview/copaw-api-chat) <br>
- [Overview / Auth / Scoping](references/overview-auth-scoping.md) <br>
- [Chats / Console Chat / SSE](references/chats-console-sse.md) <br>
- [Agents / Models / Skills / Tools](references/agents-models-skills-tools.md) <br>
- [Workspace / MCP / Cron](references/workspace-mcp-cron.md) <br>
- [Practical Recipes](references/practical-recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with endpoint sequences, JSON payload examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code is included in the skill package.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
