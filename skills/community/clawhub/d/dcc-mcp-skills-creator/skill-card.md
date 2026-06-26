## Description: <br>
Infrastructure skill for creating, validating, scaffolding, and reviewing DCC-MCP skills for the dcc-mcp-core ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold DCC-MCP skill packages, generate SKILL.md templates, and validate installable skill directories against the current dcc-mcp-core contract. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold tool writes persistent skill files under the requested parent directory. <br>
Mitigation: Choose the parent directory intentionally before invoking the tool and validate the generated skill directory before use. <br>
Risk: Generated scaffold content includes placeholders that may be incomplete for production workflows. <br>
Mitigation: Review and replace placeholder content, then run the included validation workflow before deploying generated skills. <br>


## Reference(s): <br>
- [DCC-MCP Skills Creator project homepage](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/skills/dcc-mcp-skills-creator/SKILL.md) <br>
- [DCC-MCP Skill Authoring Workflow](references/AUTHORING_WORKFLOW.md) <br>
- [DCC-MCP Tool Contracts](references/DCC_TOOL_CONTRACTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown, YAML, Python code, filesystem artifacts, and structured validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scaffold tool creates persistent files in a user-selected parent directory; validation returns issue summaries for review.] <br>

## Skill Version(s): <br>
0.18.39 (source: SKILL.md metadata.dcc-mcp.version and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
