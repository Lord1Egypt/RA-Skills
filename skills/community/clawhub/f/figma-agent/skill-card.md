## Description: <br>
Figma MCP integration for OpenClaw. Use when the user wants to read Figma designs, inspect design tokens/variables, work with Code Connect, or create/edit Figma designs. Requires one-time bootstrap setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rasimme](https://clawhub.ai/user/rasimme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design teams use Figma Agent to inspect Figma files, review design systems and variables, and create or edit screens through routed Figma MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup reuses credentials from local agent applications and stores a Figma bearer token for OpenClaw use. <br>
Mitigation: Review the bootstrap script before running it, use a dedicated or least-privileged Figma account, and install only if this credential reuse is acceptable. <br>
Risk: Write workflows can change Figma files and may produce incorrect edits if not validated. <br>
Mitigation: Back up OpenClaw configuration, manually save Figma version history before important edits, and validate each write with metadata or screenshots before reporting completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rasimme/figma-agent) <br>
- [Project homepage](https://github.com/rasimme/figma-agent) <br>
- [Figma Remote MCP server documentation](https://help.figma.com/hc/en-us/articles/32132100833559) <br>
- [Figma API reference](references/figma-api.md) <br>
- [Workflow selection](references/workflow-selection.md) <br>
- [Core rules](references/core-rules.md) <br>
- [Plugin API gotchas](references/plugin-api-gotchas.md) <br>
- [Prompting patterns](references/prompting-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, Figma MCP call patterns, and validation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an OAuth-derived Figma bearer token and validation screenshots after write operations.] <br>

## Skill Version(s): <br>
0.3.0 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
