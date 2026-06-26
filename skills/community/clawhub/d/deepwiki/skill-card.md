## Description: <br>
Query the DeepWiki MCP server for GitHub repository documentation, wiki structure, and AI-powered questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arun-8687](https://clawhub.ai/user/arun-8687) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to query documentation for public GitHub repositories, inspect wiki structure, and ask context-grounded questions through DeepWiki. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names, wiki paths, and question text are sent to DeepWiki. <br>
Mitigation: Use the skill only with public repository information and avoid including secrets, private repository details, or confidential context in prompts. <br>
Risk: The skill depends on a local Node.js runtime and the external DeepWiki service. <br>
Mitigation: Confirm Node.js is available and review returned documentation before relying on it for implementation decisions. <br>


## Reference(s): <br>
- [DeepWiki MCP documentation](https://docs.devin.ai/work-with-devin/deepwiki-mcp) <br>
- [DeepWiki MCP server](https://mcp.deepwiki.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text responses with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses depend on public repository documentation available through DeepWiki.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
