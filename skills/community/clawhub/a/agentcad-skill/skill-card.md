## Description: <br>
Agentcad Skill helps agents design, model, and build 3D objects by executing CadQuery Python scripts that produce STEP files, PNG renders, mesh exports, and geometric metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdilla1277](https://clawhub.ai/user/jdilla1277) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have agents create, run, render, inspect, export, and iterate on CadQuery-based 3D models through the local agentcad CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the separate agentcad CLI and local CadQuery/Python CAD scripts. <br>
Mitigation: Install agentcad from a trusted source, work in a project folder, and review generated CAD scripts before running them locally. <br>
Risk: Generated CAD previews, viewers, and exports may create local files or open local viewer/browser windows. <br>
Mitigation: Ask before running viewer commands when automatic browser or local viewer launch is not desired, and inspect generated outputs before sharing or manufacturing. <br>


## Reference(s): <br>
- [Agentcad documentation](https://agentcad.dev) <br>
- [Agentcad PyPI package](https://pypi.org/project/agentcad/) <br>
- [ClawHub package page](https://clawhub.ai/jdilla1277/agentcad-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; agentcad command results are JSON and generated CAD artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local STEP, PNG, STL, GLB, OBJ, HTML viewer files, and geometric metrics through agentcad.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
