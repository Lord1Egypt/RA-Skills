## Description:

Cn Todo Tracker is a Chinese-language local todo tracker for adding, completing, listing, and summarizing prioritized tasks without an account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agents use this skill to manage a local task list: add todo items, mark them done, view today or pending items, sort by priority, and review completion statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Todo text is retained locally at ~/.qclaw/workspace/todos.json until changed or removed.

Mitigation: Avoid storing confidential personal, customer, or business details unless local retention is acceptable; remove or edit saved todos when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-todo-tracker)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists todo data locally at ~/.qclaw/workspace/todos.json.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
