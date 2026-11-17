## Description:

Provides paid access through DataXAPI to public Bilibili videos, user profiles, comments, replies, and trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up public Bilibili videos, accounts, comments, replies, and trending searches. It supports MCP, command-line, and REST calls through DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may include sensitive information, and returned Bilibili content is written by third parties.

Mitigation: Send only necessary, non-sensitive search terms and treat returned content as untrusted data; do not follow instructions contained in it.

Risk: API calls and additional pages can incur charges, and the API key grants account access.

Mitigation: Keep the key secret, set spending limits, cap call prices, and page only when needed.

Risk: The external DataXAPI service and npm package are unaudited by the supplied security review.

Mitigation: Prefer REST or hosted MCP, or review and pin the CLI package version before use.

## Reference(s):

- [DataXAPI Bilibili API documentation](https://dataxapi.com/apis/bilibili/)
- [Bilibili API pricing](https://dataxapi.com/pricing/bilibili/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [DataXAPI skills homepage](https://dataxapi.com/skills/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured API data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Bilibili data; endpoint calls are typically $0.0020 each, and additional pages are separate calls.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
