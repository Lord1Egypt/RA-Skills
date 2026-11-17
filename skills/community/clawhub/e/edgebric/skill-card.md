## Description:

Search and manage your private knowledge base. Find documents, query knowledge, upload files, and manage data sources in Edgebric.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerv](https://clawhub.ai/user/jerv)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and agents use this skill to search private Edgebric knowledge bases, answer questions with citations, and manage sources or documents when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private knowledge-base content through broad searches or queries.

Mitigation: Use a read-only, source-scoped Edgebric API key for normal use and limit source access to the documents the agent should search.

Risk: API keys and private document content may be sent over insecure transport if EDGEBRIC_URL uses non-localhost HTTP.

Mitigation: Configure EDGEBRIC_URL with HTTPS for any non-localhost endpoint.

Risk: Upload, document deletion, or source deletion can change or remove knowledge-base data when the API key has elevated permissions.

Mitigation: Require explicit user confirmation before uploads or deletes, and reserve read-write or admin keys for workflows that need them.

## Reference(s):

- [Edgebric homepage](https://edgebric.com)
- [ClawHub skill page](https://clawhub.ai/jerv/skills/edgebric)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or text responses with citations, plus JSON request and response bodies for Edgebric API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform read, upload, source-management, and delete operations according to the configured Edgebric API key scope.]

## Skill Version(s):

0.9.6 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
