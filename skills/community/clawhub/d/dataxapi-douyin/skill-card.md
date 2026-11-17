## Description:

Retrieves public Douyin video, account, comment, trend, trend-index, and Xingtu data through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to look up public Douyin videos, profiles, comments, hashtags, trends, trend-index metrics, and Xingtu creator information. It helps answer questions about Douyin content, accounts, comments, and trends using DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls can incur charges, and retrieving additional pages makes additional calls.

Mitigation: Check endpoint prices before calling, set a per-call price cap, and limit paging to what the task needs.

Risk: The API key can expose a prepaid account, and search terms may contain sensitive context.

Mitigation: Use a dedicated key with a spending limit, send only necessary search terms, and never print or log the key.

Risk: The optional command-line client requires software installation; the security review does not cover the external service or CLI data handling.

Mitigation: Prefer REST or pin a reviewed CLI version, and avoid sending confidential context.

## Reference(s):

- [DataXAPI skill documentation](https://dataxapi.com/skills/)
- [DataXAPI Douyin endpoint reference](https://dataxapi.com/apis/douyin/)
- [DataXAPI Douyin pricing](https://dataxapi.com/pricing/douyin/)
- [DataXAPI MCP server](https://api.dataxapi.com/mcp)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured API data (JSON) with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are paged; each additional page requires another API call.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
