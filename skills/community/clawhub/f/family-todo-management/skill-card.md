## Description: <br>
Manage family todo lists with multi-user support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thurendous](https://clawhub.ai/user/thurendous) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Household users and agents use this skill to add, list, complete, delete, and review family todo tasks from a local Node.js command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo items and household identifiers are stored as plain local JSON data. <br>
Mitigation: Avoid putting highly sensitive information in tasks and protect or back up memory/todo.json according to the household's needs. <br>
Risk: The configured user ID fields help route tasks but are not real access controls. <br>
Mitigation: Do not rely on user IDs for security boundaries; use the skill only in trusted local or agent environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thurendous/family-todo-management) <br>
- [Publisher profile](https://clawhub.ai/user/thurendous) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Command-line text with Markdown-style todo summaries and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes todo data to a local JSON file at memory/todo.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
