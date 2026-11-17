## Description:

This skill enables agents to answer Canvas LMS questions by using the canvas-parent-mcp server to read courses, grades, assignments, announcements, planner items, conversations, and files for a user or observed student.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve and summarize Canvas LMS information for a student account or a linked observer account, including coursework, grades, announcements, conversations, planner items, and course files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill recommends unpinned third-party MCP code and fetchproxy extension access to sensitive student data.

Mitigation: Install only after reviewing and pinning trusted package and extension versions, and prefer scoped OAuth credentials over browser session cookies or passwords.

Risk: Canvas credentials and downloaded files can expose sensitive student information if stored or written carelessly.

Mitigation: Avoid storing secrets in project-local MCP configuration and download Canvas files only to an intentional safe location.

## Reference(s):

- [canvas-parent-mcp npm package](https://www.npmjs.com/package/canvas-parent-mcp)
- [canvas-parent-mcp source](https://github.com/chrischall/canvas-parent-mcp)
- [fetchproxy extension source](https://github.com/chrischall/fetchproxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with JSON configuration snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download Canvas course files to a user-selected destination path.]

## Skill Version(s):

1.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
