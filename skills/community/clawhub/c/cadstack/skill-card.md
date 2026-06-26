## Description: <br>
Generate, execute, and verify CAD scripts across FreeCAD, AutoCAD, SolidWorks, and Fusion 360 using natural language commands with safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WayneOuyang](https://clawhub.ai/user/WayneOuyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CAD automation users use this skill pack to turn natural language part requests into CAD scripts, run them against supported CAD backends, and verify generated STEP, STL, OBJ, and related model outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python CAD scripts can execute CAD operations and write model files. <br>
Mitigation: Use trusted prompts, review generated code before execution, and keep outputs in a dedicated project directory. <br>
Risk: The Fusion 360 bridge can receive CAD and export commands from local processes while it is running. <br>
Mitigation: Enable the bridge only when needed and only if you understand the local command authority it grants. <br>


## Reference(s): <br>
- [CADStack ClawHub Release](https://clawhub.ai/WayneOuyang/cadstack) <br>
- [FreeCAD](https://www.freecad.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples, configuration snippets, and CAD output file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CAD model files such as STEP, STL, OBJ, DXF, SVG, FCStd, SAT, DWG, IGES, or Parasolid depending on backend support.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
