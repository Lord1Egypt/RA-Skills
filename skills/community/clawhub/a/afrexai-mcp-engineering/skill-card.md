## Description: <br>
Build, integrate, debug, and secure MCP servers and clients in any language, enabling AI agents to call external tools via Model Context Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design, build, test, debug, and secure MCP servers and clients for agent integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adapted MCP server templates can expose excessive permissions or unsafe write, deploy, file, database, or command actions. <br>
Mitigation: Keep tools least-privilege, sandbox file and database access, and require explicit confirmation before write, deploy, or destructive actions. <br>
Risk: Secrets or credentials can leak if copied into code, configuration, logs, or tool responses. <br>
Mitigation: Store secrets outside code, pass them through environment or secret-management mechanisms, and prevent tools from returning sensitive fields. <br>
Risk: External service calls can hang, loop, or overload dependencies when templates are implemented without operational controls. <br>
Mitigation: Set timeouts, rate limits, output limits, and audit logging for MCP tools before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-mcp-engineering) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code blocks, command snippets, checklists, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated content should be reviewed before implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
