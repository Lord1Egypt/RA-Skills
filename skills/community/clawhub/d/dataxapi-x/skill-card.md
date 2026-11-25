## Description:

Retrieves public X (Twitter) posts, profiles, threads, trends, communities, lists, and video transcripts through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve public X content and account data for questions about posts, users, conversations, trends, communities, and lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint discovery may send the user's query words to DataXAPI, creating a privacy risk for confidential details.

Mitigation: Keep confidential or sensitive information out of discovery queries and review the privacy implications before sending a query.

Risk: The skill recommends running a CLI without pinning a version, and the security scan could not resolve all local references.

Mitigation: Review the referenced material and install a fixed, trusted package version before running the CLI.

Risk: API calls are billed per request and can spend the prepaid balance.

Mitigation: Check endpoint prices, tell the user the expected cost before multi-call tasks, and set a maximum price for calls.

## Reference(s):

- [DataXAPI X API documentation](https://dataxapi.com/apis/x/)
- [DataXAPI pricing for X endpoints](https://dataxapi.com/pricing/x/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)
- [ClawHub release page](https://clawhub.ai/data-x-api/skills/dataxapi-x)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON data with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live public X data; API calls may incur per-call charges.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
