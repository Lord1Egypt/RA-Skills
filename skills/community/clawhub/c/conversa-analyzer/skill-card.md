## Description:

Analyzes conversation transcripts to extract decisions, action items, dates, people, and an executive summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to turn pasted transcripts, meeting notes, chat logs, or email threads into a structured summary with decisions, action items, commitments, people, and open risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests agent memory access that is not explained or needed for transcript analysis.

Mitigation: Review before installing in environments where skills can access agent memory, and remove or limit memory access to an explicit user-selected memory record.

Risk: Conversation transcripts may contain secrets, personal identifiers, regulated data, or confidential content.

Mitigation: Redact sensitive content before submitting transcripts for analysis.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For very long inputs over 10000 characters, the skill summarizes first and then extracts structured findings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
