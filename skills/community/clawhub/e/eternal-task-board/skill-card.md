## Description: <br>
Simple CLI task/project board (kanban). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage a lightweight local kanban board from the command line, including adding, moving, listing, viewing, and removing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The task CLI rewrites the selected JSON task database when tasks change, so an unsafe --db path could overwrite an unrelated file. <br>
Mitigation: Use the default .tasks.json file or a dedicated task-file path, and avoid pointing --db at valuable or unrelated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eternal0404/eternal-task-board) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSON task database, defaulting to .tasks.json unless a custom --db path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
