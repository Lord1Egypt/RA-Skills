## Description:

Query Canvas LMS (Instructure) from a shell with curl and a bearer access token instead of running the canvas-parent-mcp server — courses, grades, assignments, submissions, calendar, planner, announcements, conversations, discussions, and files for yourself or a linked observee.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Canvas users and linked observers use this skill to retrieve course, grade, assignment, calendar, announcement, conversation, discussion, and file information from their institution's Canvas LMS through authenticated shell requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The QR login setup evaluates shell output from an unpinned package command, which could run altered or unexpected code.

Mitigation: Pin and review the login helper before use, and inspect the generated environment assignments instead of evaluating untrusted output directly.

Risk: File downloads may write to an unintended destination if the URL and output path are not validated.

Mitigation: Check that the download URL belongs to the expected Canvas host and files path, validate the destination directory, and avoid overwriting existing files.

Risk: Canvas responses can include sensitive student and account information.

Mitigation: Request only the data needed, limit where responses are stored or shared, and protect tokens and downloaded files.

Risk: Conversation lookups may change message read status.

Mitigation: Check the endpoint's read-status behavior before querying conversations, especially when preserving unread state matters.

## Reference(s):

- [Canvas API endpoint examples](references/canvas-endpoints.md)
- [ClawHub release page](https://clawhub.ai/chrischall/skills/canvas-parent-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the requested Canvas endpoint and the user's authorized account access.]

## Skill Version(s):

2.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
