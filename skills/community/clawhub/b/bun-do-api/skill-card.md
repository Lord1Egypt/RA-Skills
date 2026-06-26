## Description: <br>
Manage bun-do tasks and projects by adding, editing, deleting, toggling completion, managing subtasks, and logging project progress entries through the local bun-do REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricardofrantz](https://clawhub.ai/user/ricardofrantz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let agents manage local bun-do tasks, subtasks, recurring payments, and project progress logs while keeping task data on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to mutate or delete local task and project data. <br>
Mitigation: Require explicit user confirmation before deletes, completion changes, project creation, and log creation. <br>
Risk: The documented shell/Python search pattern could be unsafe if user-provided search text is substituted directly. <br>
Mitigation: Use safe JSON processing and proper quoting instead of interpolating raw user text into shell or Python snippets. <br>
Risk: The skill depends on a trusted local Bun Do API running on the user's machine. <br>
Mitigation: Install and use the skill only when the local Bun Do API is trusted and expected to modify the user's task data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ricardofrantz/bun-do-api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with JSON request examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local REST API instructions and command patterns for managing bun-do data.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
