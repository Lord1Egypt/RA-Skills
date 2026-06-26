## Description: <br>
Manage a team of AI sub-agents organized into departments for delegating tasks, tracking outputs, assigning roles, and coordinating multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trypto1019](https://clawhub.ai/user/Trypto1019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to organize specialized agent departments, assign tasks, track active and completed work, and generate team-level status reports for complex projects or autonomous business workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text and completion output are persisted in a local JSON file, which may expose sensitive business details if the local data directory is not appropriate for that information. <br>
Mitigation: Avoid storing secrets, credentials, or highly sensitive details in department tasks or outputs unless local storage at ~/.openclaw/department-manager/departments.json is acceptable. <br>
Risk: The skill coordinates agent tasks but does not perform quality assurance on completed outputs. <br>
Mitigation: Review completed task output before publishing, executing, or relying on it for business decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Trypto1019/arc-department-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/Trypto1019) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output and local JSON task-state data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores department and task state locally under ~/.openclaw/department-manager/departments.json by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
