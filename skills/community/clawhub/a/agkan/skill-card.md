## Description: <br>
Use when managing tasks with the agkan CLI tool - creating, listing, updating tasks, managing tags, blocking relationships, or tracking project progress with the kanban board. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gendosu](https://clawhub.ai/user/gendosu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage project work with the agkan CLI, including creating tasks, updating task state, organizing tags, tracking dependencies, and reading machine-processable task data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a local task-management CLI that can persist project task data. <br>
Mitigation: Install only if the agkan CLI is trusted, and avoid storing secrets in task bodies or metadata. <br>
Risk: Task deletion or broad board changes could remove or disrupt project planning data. <br>
Mitigation: Have the agent confirm before deleting tasks or making broad board changes. <br>


## Reference(s): <br>
- [Agkan ClawHub Skill Page](https://clawhub.ai/gendosu/agkan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with bash, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes agkan CLI commands, task workflow guidance, priority conventions, and JSON output schemas.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
