## Description:

Retrieves public Xiaohongshu (RedNote) data through DataXAPI, including notes, images, topics, users, comments, trends, creator marketplace metrics, and shop products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find and summarize public Xiaohongshu content, account activity, comments, trends, creator metrics, and shop listings through DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and discovery terms are sent to DataXAPI and may contain sensitive context.

Mitigation: Omit secrets and unnecessary personal context from queries.

Risk: Paid calls and additional pages can incur charges.

Mitigation: Set a spending budget or per-call price cap and request only the pages needed.

Risk: Using the CLI may require installing external software.

Mitigation: Prefer REST or hosted MCP, or review and pin the CLI version before installation.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [Xiaohongshu API documentation](https://dataxapi.com/apis/xiaohongshu/)
- [Xiaohongshu pricing](https://dataxapi.com/pricing/xiaohongshu/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-xiaohongshu)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured API results summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are paginated; additional pages may incur charges.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
