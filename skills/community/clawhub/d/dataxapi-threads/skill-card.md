## Description:

Retrieves public Threads posts and user data through DataXAPI for searches, post details, account profiles, and recent posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer questions about Threads content, accounts, comments, and trends by searching public posts or retrieving post and profile data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented package install is not version-pinned, and the security assessment reports incomplete analysis.

Mitigation: Review the package and pin a trusted version before installation; treat the scan as incomplete.

Risk: API calls are billed per request, including additional page requests.

Mitigation: Tell the user the expected cost before multi-call tasks and set a maximum price for calls.

Risk: Calls require a DataXAPI key and use the external DataXAPI service.

Mitigation: Use a trusted package and service, and keep the API key out of command output, logs, and URLs.

## Reference(s):

- [DataXAPI homepage](https://dataxapi.com)
- [Threads API documentation](https://dataxapi.com/apis/threads/)
- [Threads pricing](https://dataxapi.com/pricing/threads/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text responses based on structured JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-page results per API call; each additional page is a separate billable call.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
