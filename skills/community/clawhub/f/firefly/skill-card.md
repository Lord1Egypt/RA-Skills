## Description:

Fetch meeting transcripts, summaries, and action items from Firefly AI (fireflies.ai), including recent meeting lists and keyword search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codes71](https://clawhub.ai/user/codes71)

### License/Terms of Use:


## Use Case:

Employees, external collaborators, and developers use this skill to retrieve Fireflies meeting notes, summaries, transcripts, action items, and related meeting metadata through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts, summaries, participant names, and related metadata may be sensitive and can appear in terminal output or saved workspace files.

Mitigation: Use the skill only when access to Fireflies meeting data is intended, prefer explicit user confirmation before transcript retrieval, and limit custom GraphQL queries to necessary fields.

## Reference(s):

- [Firefly AI API Reference](references/api.md)
- [Fireflies GraphQL API Endpoint](https://api.fireflies.ai/graphql)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive meeting transcripts, summaries, participant names, action items, and related metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
