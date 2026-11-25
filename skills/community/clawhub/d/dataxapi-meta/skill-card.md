## Description:

Queries DataXAPI for public Meta Ad Library ads, advertisers, and video transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users, including advertisers and marketing analysts, use this skill to search public Meta Ad Library ads, look up advertisers, and retrieve ad details or video transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries are sent to DataXAPI, and the security scan was partial with package commands flagged as unpinned.

Mitigation: Avoid sensitive query details, prefer a reviewed version-pinned package, and account for the scan's incomplete coverage.

## Reference(s):

- [Meta Ad Library API documentation](https://dataxapi.com/apis/meta/)
- [Meta API pricing](https://dataxapi.com/pricing/meta/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured API data with concise textual summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results describe public Meta Ad Library data; include the data source and retrieval time in user-facing answers.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
