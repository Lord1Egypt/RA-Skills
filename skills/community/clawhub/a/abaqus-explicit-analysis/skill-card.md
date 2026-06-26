## Description: <br>
Abaqus/Explicit-focused skill for transient nonlinear finite element analysis, including drop, impact, blast, forming, model setup, contact, stability, energy-balance validation, troubleshooting, and a runnable drop-simulation script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jijinbao-code](https://clawhub.ai/user/jijinbao-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Engineers and developers use this skill to plan and script Abaqus/Explicit simulations for high-speed transient nonlinear problems such as drop tests, impacts, blast, forming, and large-deformation contact. It helps configure model setup, materials, elements, contact, solver jobs, and result checks for energy balance, hourglass energy, contact penetration, and timestep stability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the included Abaqus script can consume local CPU, memory, license tokens, and disk space. <br>
Mitigation: Confirm Abaqus license availability and adjust CPU, memory, mesh, analysis time, output frequency, and job settings for the target workstation or shared compute environment before execution. <br>
Risk: Default simulation settings may not match the user's hardware, material assumptions, contact conditions, or intended physical scenario. <br>
Mitigation: Review and adapt material data, contact definitions, boundary conditions, initial velocity or gravity setup, and validation checks before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jijinbao-code/abaqus-explicit-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/jijinbao-code) <br>
- [Abaqus/Explicit product page](https://www.3ds.com/products/simulia/abaqus/explicit) <br>
- [SIMULIA resource center](https://www.3ds.com/products/simulia/resource-center) <br>
- [Abaqus user documentation mirror referenced by the skill](https://abaqus.uclouvain.be/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Abaqus/CAE Python script patterns and solver/job setting recommendations.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
