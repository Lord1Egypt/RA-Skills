## Description: <br>
Control Blender from the shell via Flue - a Python bridge to bpy without an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfkislev](https://clawhub.ai/user/sfkislev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill when they want an agent to inspect or make bounded edits inside Blender scenes through Flue and Blender's bpy runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flue can automate Blender through its scripting runtime and may change open scene content. <br>
Mitigation: Use small, inspectable steps and review changes before saving important Blender work. <br>
Risk: The setup flow may require installing and configuring the Flue Python package. <br>
Mitigation: Review Flue before setup and require explicit approval before running pip install or setup commands. <br>


## Reference(s): <br>
- [Flue GitHub Repository](https://github.com/SFKislev/flue) <br>
- [ClawHub Skill Page](https://clawhub.ai/sfkislev/blender-flue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to send Python scripts to Blender through Flue and receive structured JSON results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
