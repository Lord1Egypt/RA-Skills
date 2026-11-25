## Description:

Retrieves public YouTube videos, posts, channels, and comments through DataXAPI for questions about YouTube content, accounts, comments, or trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve public YouTube video, channel, post, comment, and transcript data through DataXAPI, then answer questions or summarize the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint discovery may send user-provided words to DataXAPI, a third party.

Mitigation: Tell the user before discovery and limit requests to the necessary, non-sensitive search terms.

Risk: The install command uses an unpinned package, and the security review has incomplete coverage.

Mitigation: Review and pin the package version before installation, and inspect unresolved local references before relying on the scan.

## Reference(s):

- [DataXAPI YouTube API documentation](https://dataxapi.com/apis/youtube/)
- [DataXAPI YouTube pricing](https://dataxapi.com/pricing/youtube/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [DataXAPI response JSON with public YouTube text and metadata, summarized as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; additional pages incur additional charges.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
