## Description:

Mock technical interview mode for OpenAlgernon that simulates a senior AI engineering interviewer with adaptive difficulty, follow-up probes, and a full scored report at the end.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniovfranco](https://clawhub.ai/user/antoniovfranco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to practice technical interviews on OpenAlgernon study materials and receive calibrated category scores, weak-response notes, and study recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interview summaries may be written to the OpenAlgernon memory directory without explicit confirmation at the end of each session.

Mitigation: Require user confirmation before saving memory entries, or disable memory writes for sensitive interview practice.

Risk: When Notion export variables are configured, full interview reports may be appended to Notion.

Mitigation: Ask for confirmation before exporting, review the report content, and verify the target Notion page before appending.

Risk: Material slugs are used to query the local study database.

Mitigation: Validate material slugs against known OpenAlgernon materials before querying.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational interview prompts followed by a Markdown-style scored report and optional shell command examples for saving or exporting results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append a short session memory entry under the OpenAlgernon memory directory and may append the full report to Notion when the relevant environment variables and CLI are configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
