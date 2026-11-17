## Description:

Public TikTok data through DataXAPI: videos, hashtags, users, comments, ad library, Creative Center, TikTok Shop. 18 endpoints, $0.0020 a call, a failed call is free. Use when the user asks about TikTok content, accounts, comments or trends, or gives a TikTok link, ID or account name. 通过 DataXAPI 取TikTok的公开数据：视频、话题、用户、评论、广告库、创意中心、TikTok Shop。18 个接口，一次 $0.0020，失败不收费。用户问到TikTok的内容、账号、评论或热点，或给出TikTok的链接、编号、账号名时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this agent skill to retrieve public TikTok videos, hashtag posts, user profiles, comments, ads, and TikTok Shop listings through DataXAPI. It also helps identify suitable endpoints and their prices before making paid calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may reveal private context to the data service.

Mitigation: Use public search terms and exclude private context from discovery queries.

Risk: Pagination creates additional paid calls.

Mitigation: Set spending limits, cap multi-call requests with max_price, and tell the user the cost before making calls that add up.

Risk: Installing or running the CLI adds a software dependency.

Mitigation: Prefer REST or remote MCP, or pin a reviewed CLI version.

## Reference(s):

- [DataXAPI TikTok API documentation](https://dataxapi.com/apis/tiktok/)
- [DataXAPI TikTok pricing](https://dataxapi.com/pricing/tiktok/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [Structured API responses and Markdown guidance with JSON, shell, and REST examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-call results; additional pages incur additional charges.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
