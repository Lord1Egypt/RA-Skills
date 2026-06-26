## Description: <br>
Guides agents through Abaqus analysis solving workflows, including Standard and Explicit solver selection, analysis step setup, solution controls, job management, and parallel computation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jijinbao-code](https://clawhub.ai/user/jijinbao-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and simulation engineers use this skill to choose Abaqus solvers, configure analysis steps, monitor solver behavior, manage jobs, and tune parallel execution for finite element analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect model paths, resource settings, or license assumptions could cause failed or unintended Abaqus job execution. <br>
Mitigation: Confirm the model, working directory, CPU count, memory setting, and Abaqus license environment before running any generated job commands. <br>
Risk: Solver guidance can be misapplied to unsuitable Standard or Explicit analysis cases. <br>
Mitigation: Review the selected solver, analysis step, convergence controls, and energy checks against the specific finite element model before deployment. <br>


## Reference(s): <br>
- [Abaqus official documentation](https://help.3ds.com) <br>
- [Abaqus/Standard](https://www.3ds.com/products/simulia/abaqus/standard) <br>
- [Abaqus/Explicit](https://www.3ds.com/products/simulia/abaqus/explicit) <br>
- [ClawHub skill page](https://clawhub.ai/jijinbao-code/abaqus-solving) <br>
- [Publisher profile](https://clawhub.ai/user/jijinbao-code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with tables, bullet lists, and inline Python job configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; validate Abaqus model, working directory, CPU and memory settings, and license environment before running proposed job commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
