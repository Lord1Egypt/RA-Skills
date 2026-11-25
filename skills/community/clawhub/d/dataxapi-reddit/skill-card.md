## Description:

Retrieves public Reddit posts, comments, user and community details, trends, and video captions through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve public Reddit content for questions about posts, comments, accounts, communities, and trends. The skill supports search, profile and post lookups, comment threads, trending searches, and Reddit-hosted video captions through DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint discovery may send the user's query wording to DataXAPI.

Mitigation: Review the privacy implications of discovery and avoid including private details in queries.

Risk: The recommended package installation is not version-pinned, and the security scan was partial.

Mitigation: Install only a reviewed, exact DataXAPI package version and account for the scan's unresolved local references.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [Reddit API endpoints](https://dataxapi.com/apis/reddit/)
- [Reddit endpoint pricing](https://dataxapi.com/pricing/reddit/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-reddit)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured JSON data, with text or Markdown summaries for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each API page is a separately billed call; additional pages use a cursor.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
