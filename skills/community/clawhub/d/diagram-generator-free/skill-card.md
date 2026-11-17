## Description: <br>
Diagram基础版 helps agents turn natural-language diagram requests into JSON specifications and generate basic Mermaid flowcharts or Draw.io architecture diagrams through the mcp-diagram-generator MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and product teams use this skill to quickly document simple workflows and basic application architecture as Mermaid or Draw.io files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires configuring and running the mcp-diagram-generator MCP package through npx. <br>
Mitigation: Install it only in environments where running that MCP package is acceptable, and review the MCP configuration before use. <br>
Risk: The skill writes generated diagram files to local diagrams/mermaid/ or diagrams/drawio/ directories. <br>
Mitigation: Confirm the working directory and expected output paths before generation, then review generated files before committing or sharing them. <br>
Risk: The instructions are primarily in Chinese, which may cause misuse by readers who do not understand the language. <br>
Mitigation: Translate the instructions before use if needed, and verify the requested diagram type, filename, and output format. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-generator-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with JSON specifications, MCP configuration examples, and generated Mermaid or Draw.io files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are expected under local diagrams/mermaid/ or diagrams/drawio/ directories when the MCP server is configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
