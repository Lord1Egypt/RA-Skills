## Description:

Manage persistent project todos in markdown files under the todos/ directory for creating, triaging, tracking dependencies, work logs, and completion status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to maintain persistent project todo files for backlog items, code review follow-ups, PR feedback, dependencies, and implementation work logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to create and rename markdown files under todos/, which can introduce persistent repository changes.

Mitigation: Review generated or renamed todo files before committing them.

Risk: Todo filenames and YAML frontmatter can drift if status, priority, or issue IDs are edited inconsistently.

Mitigation: Verify that issue_id is unique and that status and priority match both the filename and frontmatter before considering a todo complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-file-todos)
- [Todo Workflows](artifact/references/workflows.md)
- [Quick Reference Commands](artifact/references/quick-reference.md)
- [Todo Template](artifact/assets/todo-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown todo files with YAML frontmatter plus concise command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists task state by creating, editing, and renaming markdown files under todos/.]

## Skill Version(s):

4.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
