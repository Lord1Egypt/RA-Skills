## Description:

Automated development workflow with task board management, code quality checks, and continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run scheduled, task-board-driven code improvement loops that select one task, make bounded code changes, run checks and tests, update the task board, and report results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically reset, edit, push, and possibly deploy code without enough safeguards.

Mitigation: Install it only in a disposable or well-protected repository, preferably on a dedicated branch or isolated worktree with backups, review gates, limited credentials, and no direct protected-branch push or production deployment credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update repository files and task-board state when applied by an agent.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
