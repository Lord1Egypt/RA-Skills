## Description: <br>
Manage Todoist tasks using the `todoist` CLI to add, list, and complete tasks from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to manage Todoist tasks by listing pending items, adding tasks with optional due dates, and marking tasks complete through a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Todoist tasks when task-account credentials are available. <br>
Mitigation: Use a narrowly scoped Todoist token and enable the skill only where task reads and writes are expected. <br>
Risk: The artifact mentions Microsoft Graph token use, but server security guidance says the Microsoft To-Do behavior is unclear. <br>
Mitigation: Do not provide a Microsoft Graph token unless the publisher clearly documents and validates Microsoft To-Do support. <br>
Risk: Installation depends on a Todoist CLI provided through the `todoist-api-python` package. <br>
Mitigation: Verify the package source and installed `todoist` command before enabling the skill for an agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xejrax/brainz-tasks) <br>
- [Publisher profile](https://clawhub.ai/user/Xejrax) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment-variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `todoist` command and a supported task-service token before task commands can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
