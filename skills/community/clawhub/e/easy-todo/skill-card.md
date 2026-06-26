## Description: <br>
Personal TODO list manager. Add tasks with deadlines and priorities, mark them done, set up recurring items, and receive morning and evening summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simenfur](https://clawhub.ai/user/simenfur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and their agents use this skill to maintain a local personal TODO list, track deadlines and priorities, manage recurring tasks, and receive morning or evening summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task titles, notes, and schedules are stored on local disk. <br>
Mitigation: Do not store secrets or highly sensitive notes in tasks, and review the local todos.md file location before use. <br>
Risk: Morning and evening briefings depend on the agent environment actually running scheduled commands. <br>
Mitigation: Confirm scheduled execution support in the host agent before relying on proactive reminders. <br>
Risk: Changing TODOS_FILE can redirect where task data is written. <br>
Mitigation: Leave TODOS_FILE unset unless intentionally using a different task-store path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/simenfur/easy-todo) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/simenfur) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Plain text command output and a local Markdown TODO file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and writes task data to a local todos.md file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
