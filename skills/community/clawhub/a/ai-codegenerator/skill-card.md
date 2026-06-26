## Description: <br>
Automatically generates a small FastAPI project scaffold from a user-provided task description, with optional context and constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason513597](https://clawhub.ai/user/jason513597) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to generate a basic FastAPI application scaffold from a task description, then review and adapt the generated files for their project requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated project files may require review before they are run or used in a larger application. <br>
Mitigation: Review the generated FastAPI files and dependency pins before running, deploying, or integrating them. <br>
Risk: The skill writes generated projects under the configured OpenClaw workspace path. <br>
Mitigation: Confirm the target workspace location is appropriate and inspect generated paths before using the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason513597/ai-codegenerator) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Markdown, Configuration, JSON] <br>
**Output Format:** [Generated FastAPI project files plus a JSON execution summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates requirements.txt, README.md, app/__init__.py, and app/main.py under the configured OpenClaw workspace path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
