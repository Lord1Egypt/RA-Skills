## Description:

Summarize a user's recent Feishu work into a concise weekly review or time-machine recap by reading Feishu docs, meeting notes, and related materials, then separating the user's real work from meeting noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihiue](https://clawhub.ai/user/nihiue)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers use this skill to turn recent Feishu documents, meeting notes, and project materials into concise weekly or monthly work reviews. It helps distinguish actual user-owned work from general meeting participation and can draft or update a Feishu document when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read sensitive Feishu work documents and meeting materials while preparing a work review.

Mitigation: Use it only with Feishu materials the agent is allowed to read, and limit the requested scope to the documents and time period needed for the review.

Risk: When asked to create or update a Feishu document, the agent may overwrite draft content the user cares about.

Mitigation: Specify the exact target document and review the generated draft before allowing updates or overwrites.

Risk: Meeting attendance or unsupported AI-generated meeting summaries can be mistaken for user-owned work.

Mitigation: Prefer ownership signals such as document authorship, assigned action items, primary speaker role, and repeated evidence across documents; use softer wording when ownership is uncertain.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries, with optional Feishu document drafting or revision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are concise Chinese work-review summaries by default unless the user requests another language or level of detail.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
