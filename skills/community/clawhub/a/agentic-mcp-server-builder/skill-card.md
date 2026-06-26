## Description: <br>
Scaffold MCP server projects and baseline tool contract checks for defining tool schemas, generating starter server layouts, and validating MCP-ready structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to define MCP tool contracts and generate a minimal starter server layout before adding business logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold script can write generated files in the selected scaffold root. <br>
Mitigation: Use a dedicated project directory, run with --dry-run first, and avoid --allow-outside-workspace unless intentionally needed. <br>
Risk: Sensitive existing paths could receive generated output if selected as --output or scaffold_root. <br>
Mitigation: Keep generated paths inside the workspace by default and do not set --output or scaffold_root to sensitive existing paths. <br>


## Reference(s): <br>
- [MCP Scaffold Guide](references/mcp-scaffold-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/0x-Professor/agentic-mcp-server-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [JSON, Markdown, or CSV artifacts plus starter scaffold files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode can report the planned file map without writing scaffold files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
