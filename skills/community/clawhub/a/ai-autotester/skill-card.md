## Description: <br>
Automates testing for trusted Python projects by preparing basic pytest files, installing dependencies, running tests, and returning a concise result summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason513597](https://clawhub.ai/user/jason513597) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to add and run a basic smoke-test workflow for trusted Python projects, then review the generated test report, logs, and summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify repository files while preparing tests and dependency files. <br>
Mitigation: Run it in a disposable branch, container, or temporary copy and review file changes before keeping them. <br>
Risk: The skill can install Python packages and execute project tests on the host. <br>
Mitigation: Use it only with trusted projects and prefer an isolated virtual environment or container. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason513597/ai-autotester) <br>
- [Publisher profile](https://clawhub.ai/user/jason513597) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Files] <br>
**Output Format:** [JSON status report with generated pytest files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes target path, return code, truncated pytest stdout and stderr, and a UTC timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
