## Description:

This skill should be used when the user asks about Canvas LMS data — their own student account or any observed student.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and other Canvas observers use this skill to review courses, grades, assignments, deadlines, announcements, conversations, and files for their own account or linked students.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canvas results can include grades, submissions, conversations, and files for the account or linked students.

Mitigation: Confirm the intended Canvas account and linked student before retrieval, and review results before sharing them.

Risk: Setup may use browser session cookies, access tokens, OAuth credentials, or passwords.

Mitigation: Review the setup instructions, select an authentication method supported by the institution, and keep its credentials private.

## Reference(s):

- [canvas-parent-mcp package](https://www.npmjs.com/package/canvas-parent-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Canvas data summaries, records, file links, or downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include Canvas records and expiring download links.]

## Skill Version(s):

2.3.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
