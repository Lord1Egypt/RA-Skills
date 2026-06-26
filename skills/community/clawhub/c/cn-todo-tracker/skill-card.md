## Description: <br>
Cn Todo Tracker helps agents manage Chinese-language todo items with local commands to add, complete, list, and summarize tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users and agents can use this skill to track personal or work todo items through a local Python CLI. It supports adding tasks, marking them complete, listing current or today's items, and summarizing completion statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo entries may contain private or sensitive information because the skill stores user-provided task text locally. <br>
Mitigation: Avoid storing secrets or confidential data in todo items, and review or remove ~/.qclaw/workspace/todos.json before sharing the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-todo-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Markdown text with optional shell commands and local JSON todo data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When commands are executed, todo records are stored locally at ~/.qclaw/workspace/todos.json.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
