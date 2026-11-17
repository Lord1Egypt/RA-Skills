## Description:

Simple CLI task/project board (kanban).

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual contributors use this skill to maintain a lightweight local kanban board from the command line, including adding, listing, moving, viewing, and removing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data is stored in a local JSON file, and removing a task permanently changes that database unless a backup exists.

Mitigation: Use a deliberate database path and keep a backup of the task database before removing tasks.

Risk: The --db option can write task data to a different local path than the default .tasks.json.

Mitigation: Review the selected --db path before running commands, especially in shared or multi-project workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eternal0404/skills/eternal-task-board)
- [Publisher profile](https://clawhub.ai/user/eternal0404)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with a local JSON task database]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task state in .tasks.json by default, or in the local path supplied with --db.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
