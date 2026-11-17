## Description:

A conversational todo-list skill that manages tasks with GTD and Eisenhower-style priorities, contexts, weights, due dates, aliases, and text-formatted lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtyatno](https://clawhub.ai/user/mtyatno)

### License/Terms of Use:


## Use Case:

Agent users use this skill to capture, update, complete, and filter personal or work tasks in a structured chat workflow. It is useful when a lightweight local todo protocol is preferred over an external task-management service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's implementation may write task data to a sibling claw-todolist folder rather than the installed skill folder.

Mitigation: Review the storage path before installation and avoid using the skill for sensitive tasks until the persistence location is fixed or clearly documented.

Risk: The advertised REVIEW command may not match the implemented command router.

Mitigation: Test expected commands during installation review and rely only on verified task add, complete, edit, and show behavior until REVIEW support is implemented or removed from documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtyatno/skills/claw-todolist)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Plain text and Markdown-style task lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local JSON task state and formats active tasks by priority, context, weight, and due date.]

## Skill Version(s):

1.4.1 (source: server release evidence; artifact package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
