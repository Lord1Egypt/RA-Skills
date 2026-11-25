## Description:

Retrieves public Facebook page, post, and comment data through DataXAPI for questions about Facebook content, accounts, and trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve and summarize public Facebook page profiles, posts, post details, and comments when asking about accounts, content, or trends. Calls use DataXAPI's per-call pricing, with controls for limiting spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery queries are sent to DataXAPI, and suggested CLI install commands do not pin a package version.

Mitigation: Keep private or confidential details out of discovery queries, and verify the package source and version before installing.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [Facebook API documentation](https://dataxapi.com/apis/facebook/)
- [Facebook API pricing](https://dataxapi.com/pricing/facebook/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [ClawHub release](https://clawhub.ai/data-x-api/skills/dataxapi-facebook)

## Skill Output:

**Output Type(s):** [JSON data, Text summaries, Guidance]

**Output Format:** [JSON API responses summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Facebook page, post, and comment data; paginated results where supported.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
