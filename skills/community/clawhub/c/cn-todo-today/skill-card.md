## Description: <br>
Cn Todo Today is a pure-Python local todo-list skill for adding, listing, completing, deleting, and viewing stats for daily todos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users can use this skill to manage a local daily todo list from an agent or shell workflow, including adding items, listing today's work, marking items complete, deleting items, and checking completion stats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo text is stored locally in plain JSON at ~/.cn_todo_today.json. <br>
Mitigation: Avoid storing secrets or sensitive personal information in todo text, and review local file permissions where needed. <br>
Risk: The skill creates and modifies a home-directory JSON file. <br>
Mitigation: Review the target path before use and back up or inspect the file if local todo data is important. <br>
Risk: Some documented command examples omit flags required by the script. <br>
Mitigation: Use --text for add commands and --id for done or delete commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-todo-today) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; script output is terminal text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and modifies a local JSON todo store at ~/.cn_todo_today.json when the documented commands are run.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
