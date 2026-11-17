## Description:

Transforms pasted meeting notes, transcripts, email threads, or chat exports into concise summaries, action items with owners and deadlines, decisions, saved Markdown notes, and an optional to-do tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffjhunter](https://clawhub.ai/user/jeffjhunter)

### License/Terms of Use:


## Use Case:

Employees and external users can use this skill to turn unstructured meeting records into summaries, follow-up tasks, owner/deadline assignments, decisions, and searchable Markdown notes. It is also useful for maintaining a local to-do list derived from meeting action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves complete raw meeting content by default, which can expose confidential meetings, customer data, HR or legal topics, financial details, or credentials if used in an untrusted workspace or shared downstream.

Mitigation: Use it only in trusted workspaces, request no-save or summary-only handling when appropriate, and manually redact sensitive transcript content before sharing saved notes or generated summaries.

Risk: Extracted owners, deadlines, and decisions may be incomplete or incorrect when source notes are messy or ambiguous.

Mitigation: Review generated summaries, action items, owners, deadlines, and decisions before relying on them for follow-up or adding them to todo.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffjhunter/skills/ai-meeting-notes)
- [Publisher homepage](https://jeffjhunter.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown notes, concise chat summaries, task lists, optional JSON/table/Slack/email variants, and workspace files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates date-prefixed meeting note files under meeting-notes/ and can update a root-level todo.md when the user chooses action items to track.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
