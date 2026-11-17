## Description:

Generates structured Chinese meeting minutes from a Feishu Minutes link, minute token, or transcript file, with optional PDF export and Feishu Drive upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfvincentyang](https://clawhub.ai/user/jfvincentyang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and agents use this skill to turn Feishu meeting records or local transcripts into reviewable Chinese meeting minutes, action items, and optional PDF deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Feishu meeting records and transcripts through lark-cli scopes.

Mitigation: Grant only the documented Feishu scopes needed for the intended workflow and use the upload scope only when PDF upload is required.

Risk: Generated minutes can contain sensitive meeting details, participant names, transcript paths, Feishu tokens, or links.

Mitigation: Review the generated Markdown and PDF before distribution or upload, and remove sensitive content that should not be shared.

Risk: Automatic transcript summarization may omit context or produce incorrect action items.

Mitigation: Compare the generated minutes with the original transcript before treating decisions, owners, and deadlines as final.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jfvincentyang/skills/feishu-meeting-minutes)
- [Meeting minutes template](references/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown meeting minutes, optional PDF file, and command output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local meeting_minutes_YYYYMMDD_<slug>_<token>.md files and optional PDFs; optional upload returns Feishu Drive command output.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
