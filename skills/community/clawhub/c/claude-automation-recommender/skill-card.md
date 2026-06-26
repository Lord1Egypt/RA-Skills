## Description: <br>
Analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, plugins, MCP servers). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinhltt](https://clawhub.ai/user/vinhltt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze a project and choose practical Claude Code automations for hooks, subagents, skills, plugins, and MCP servers. It produces a concise recommendation report tailored to detected frameworks, tools, workflows, and project patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommended hooks, plugins, MCP servers, or generated skill configurations could affect repositories, external services, databases, containers, cloud resources, or team workflows if enabled without review. <br>
Mitigation: Treat recommendations as proposals; inspect each automation before enabling it, avoid committing secrets in .mcp.json, use least-privilege tokens and read-only modes, and require explicit review for tools with side effects. <br>
Risk: Shared configuration recommendations such as .mcp.json or hooks can affect an entire team. <br>
Mitigation: Review shared settings before committing them and keep credentials out of repository-managed configuration. <br>


## Reference(s): <br>
- [Hooks Recommendations](artifact/references/hooks-patterns.md) <br>
- [MCP Server Recommendations](artifact/references/mcp-servers.md) <br>
- [Plugin Recommendations](artifact/references/plugins-reference.md) <br>
- [Skills Recommendations](artifact/references/skills-reference.md) <br>
- [Subagent Templates](artifact/references/subagent-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with inline shell commands, configuration snippets, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only recommendations; users implement suggested automations separately.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
