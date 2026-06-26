## Description: <br>
Execute tasks end-to-end while respecting safety boundaries, completing in-scope subtasks autonomously while confirming sensitive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pouyakhodadust-eng](https://clawhub.ai/user/pouyakhodadust-eng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent complete clearly scoped, in-workspace subtasks end to end while escalating sensitive or ambiguous actions for confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages autonomous progress, which can exceed user intent when the task or workspace scope is unclear. <br>
Mitigation: Use a clearly scoped task and workspace, and pause for user input when scope is missing, ambiguous, or outside the workspace. <br>
Risk: Sensitive actions such as sending messages, deleting data, accessing credentials, changing system settings, or using elevated commands can create security or user-impact risk. <br>
Mitigation: Require explicit user confirmation before sensitive actions and stop rather than attempting to bypass authentication or credential errors. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown guidance and concise progress or completion reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; generated files, commands, or configuration changes depend on the user's task and require confirmation for sensitive actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
