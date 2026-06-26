## Description: <br>
A structured, conversational todo-list manager based on GTD and Eisenhower that manages local task state with aliases, priority groups, weight markers, due dates, and weekly review output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtyatno](https://clawhub.ai/user/mtyatno) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users can use this skill to manage conversational todo lists with priority, context, weight, due-date, completion, edit, filter, and review commands. It is intended for local task organization rather than shared project management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo text is persisted locally in the skill folder and may contain sensitive personal or work details. <br>
Mitigation: Avoid entering secrets or sensitive data into todo text, and install only where local task persistence is acceptable. <br>
Risk: Short aliases such as a, x, ls, and e can modify or reveal the saved todo list when used deliberately. <br>
Mitigation: Review commands before use, especially add, edit, and done operations that change local state. <br>
Risk: Bundled import_tasks.txt contains example task entries that may not apply to the user. <br>
Mitigation: Inspect or ignore bundled example tasks before importing or adapting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mtyatno/claw-todolist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Plain text and Markdown-formatted task lists, status messages, filters, and review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores todo state locally in the skill folder and formats active tasks by priority, context, weight, and due date.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
