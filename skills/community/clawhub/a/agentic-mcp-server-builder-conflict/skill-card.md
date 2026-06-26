## Description: <br>
Scaffold MCP server projects, define tool schemas, generate starter layouts, and validate MCP-ready structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuradil](https://clawhub.ai/user/nuradil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create a minimal MCP server scaffold, summarize tool contracts, and review baseline checks before adding business logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold script can create starter files and overwrite the fixed starter filenames it manages in non-dry-run mode. <br>
Mitigation: Run the script with --dry-run first and point scaffold_root and --output at a new project directory. <br>
Risk: The --allow-outside-workspace option permits scaffold_root to resolve outside the current workspace. <br>
Mitigation: Use --allow-outside-workspace only when deliberately writing outside the workspace and after checking the target path. <br>


## Reference(s): <br>
- [MCP Scaffold Guide](artifact/references/mcp-scaffold-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated JSON, Markdown, CSV, and starter files when the bundled script is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scaffold script can run in dry-run mode and can write fixed starter filenames in a selected project directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
