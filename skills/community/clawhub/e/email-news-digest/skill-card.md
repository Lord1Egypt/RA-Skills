## Description:

Summarize recent emails, generate a thematic image, and send a formatted HTML email report with the summary and image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxfz3](https://clawhub.ai/user/matthewxfz3)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn a targeted Gmail query into an email digest with a structured summary, generated image, and formatted HTML report sent to chosen recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs Gmail mailbox access and can send outbound email to supplied recipients.

Mitigation: Use narrowly targeted Gmail queries and trusted recipient lists only, and review recipients before execution.

Risk: The current summarizer is a placeholder and may send digest content that is unrelated to the selected email.

Mitigation: Avoid confidential, regulated, or business-critical mail until a true input-based summarizer and preview or confirmation step are added.

Risk: Temporary files and generated artifacts may contain decoded email content or report material during processing.

Mitigation: Run the skill only in trusted environments and improve temporary-file handling before use with sensitive mailbox content.

## Reference(s):

- [Email Filters Reference](references/email-filters.md)
- [HTML Email Template](references/html-template.html)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Markdown, Files, Configuration]

**Output Format:** [Markdown guidance with inline bash commands; runtime output includes a generated image file, structured summary JSON, and an HTML email body.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires recipient addresses, a Gmail search query, and an image prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
