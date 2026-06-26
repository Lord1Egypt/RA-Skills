## Description: <br>
Agentcad is a CAD tool for AI agents that helps agents design, model, and build 3D objects by running build123d or CadQuery Python scripts to produce STEP files, PNG renders, mesh exports, and geometric metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdilla1277](https://clawhub.ai/user/jdilla1277) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to ask an agent to create or iterate on CAD models, validate geometry, render previews, export mesh formats, and share generated model files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to execute local CAD Python scripts through the agentcad CLI. <br>
Mitigation: Install it only when local CAD script execution is intended, review generated scripts before execution, and use dry runs or inspection commands to validate geometry before sharing outputs. <br>
Risk: The workflow may open generated previews or viewers in a browser. <br>
Mitigation: Ask before running `agentcad view` in environments where opening browser windows is not desired. <br>


## Reference(s): <br>
- [agentcad documentation](https://agentcad.dev) <br>
- [agentcad PyPI package](https://pypi.org/project/agentcad/) <br>
- [ClawHub skill page](https://clawhub.ai/jdilla1277/agentcad) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python CAD code, and generated CAD artifact paths from JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce STEP files, PNG previews, STL/GLB/OBJ mesh exports, interactive viewer HTML, and geometry metrics through the local agentcad CLI.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
