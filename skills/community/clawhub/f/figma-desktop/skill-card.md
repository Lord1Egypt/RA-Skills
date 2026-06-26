## Description: <br>
Figma Desktop MCP Skill that helps agents connect to Figma Desktop's local MCP server to access Figma Make, code generation, Code Connect, design-system, and file-context capabilities without OAuth setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuel-qin](https://clawhub.ai/user/samuel-qin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design engineers use this skill to configure an agent to work with a local Figma Desktop MCP server, inspect open Figma files, generate code from selected designs, and run design-system or Code Connect workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent connected through Figma Desktop MCP can act through the user's logged-in Figma session and access files that are open in the desktop app. <br>
Mitigation: Use the skill only with intended files, avoid confidential designs during testing, and disable the MCP server when it is not needed. <br>
Risk: Optimization, synchronization, and generation commands may change design or project state. <br>
Mitigation: Confirm the target selection and intended operation before running state-changing commands. <br>
Risk: The workflow depends on installing and invoking the external mcporter CLI. <br>
Mitigation: Verify the mcporter package source before installation and keep the installation scoped to trusted environments. <br>


## Reference(s): <br>
- [Figma Desktop Downloads](https://www.figma.com/downloads/) <br>
- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/) <br>
- [Introducing Figma MCP Server](https://www.figma.com/blog/introducing-figma-mcp-server/) <br>
- [Figma Code Connect Documentation](https://developers.figma.com/code-connect/) <br>
- [ClawHub Skill Page](https://clawhub.ai/samuel-qin/figma-desktop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Figma Desktop to be running with a design or FigJam file open and the local MCP server enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
