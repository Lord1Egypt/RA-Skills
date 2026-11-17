## Description:

Provides public WeChat Channels video, account, collection, comment, and search lookups through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to look up public WeChat Channels videos, accounts, collections, comments, and search results through DataXAPI. Calls are paid per endpoint, so users should be told the cost before multi-page lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and selected WeChat identifiers are sent to DataXAPI.

Mitigation: Keep private or sensitive context out of discovery queries.

Risk: Paid calls can consume prepaid credit, including calls that return empty lists, and pagination incurs another call.

Mitigation: Tell users the price before multi-page lookups and set a per-call spending cap.

Risk: The external CLI and setup instructions have not been verified.

Mitigation: Prefer REST or MCP, or review and pin the CLI release before use.

## Reference(s):

- [DataXAPI WeChat Channels API reference](https://dataxapi.com/apis/wechat_channels/)
- [DataXAPI WeChat Channels pricing](https://dataxapi.com/pricing/wechat_channels/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text or Markdown summaries based on structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A page is returned per call; calls may cost $0.02, and some empty results are also charged.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
