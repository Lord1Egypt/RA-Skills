## Description:

Query and search medical records from CareMax Health API with structured queries and AI-powered semantic search using retrieval-augmented answers with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kittenyang](https://clawhub.ai/user/kittenyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find, query, and ask questions about CareMax medical records, including check-up history, hospital visits, test results, gene reports, and specific record details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health data and may process medical questions, record excerpts, and generated answers through AI/search backends.

Mitigation: Install only after reviewing the CareMax API data flow and confirming that users are comfortable with AI/search processing of medical-record content.

Risk: The skill depends on a separate caremax-auth package with authentication scripts that were not audited in this artifact.

Mitigation: Review or pin the caremax-auth package and authentication scripts before installation or use.

Risk: Chat interactions are automatically retained and the skill includes commands that can delete individual chats or all chat history.

Mitigation: Require explicit user confirmation before deleting chat history, especially before clearing all history.

## Reference(s):

- [CareMax Records on ClawHub](https://clawhub.ai/kittenyang/skills/caremax-records)
- [Publisher profile: kittenyang](https://clawhub.ai/user/kittenyang)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include medical-record excerpts, generated answers, citations, and chat-history operations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
