## Description: <br>
Bootstraps new Model Context Protocol (MCP) servers from a natural language description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asimons81](https://clawhub.ai/user/asimons81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold MCP servers and tools from natural language requirements, including project files, tool definitions, configuration snippets, and test examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated project files and MCP configuration may not match the user's target runtime or security expectations until reviewed. <br>
Mitigation: Use the skill in a new or clearly chosen project directory, then review generated package files, tool schemas, and MCP configuration before running them. <br>
Risk: A generated MCP server may require credentials or environment-specific access after scaffolding. <br>
Mitigation: Provide credentials only after reviewing the generated server behavior and only when the target integration explicitly requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asimons81/agentic-atlas-mcp-builder) <br>
- [Publisher profile](https://clawhub.ai/user/asimons81) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scaffolded TypeScript or Python MCP server files, tool schemas, test harness examples, and agent configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
