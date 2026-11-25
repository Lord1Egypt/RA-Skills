## Description:

Search public Douyin content in real time to retrieve video and image-text posts, engagement metrics, trends, and comments for brand, topic, event, or content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, social media operators, and content analysts use this skill to research public Douyin posts, creators, comments, and trending topics for content planning, market research, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends supplied search terms, links, or IDs to the third-party Guaikei API; the security guidance also notes keyword-based account discovery.

Mitigation: Use public-content queries only, and avoid sending confidential terms or identifiers unless they are appropriate to share with the service.

Risk: The security scan reports medium confidence and partial analysis, with some components not fully inspected.

Mitigation: Review the skill before deployment and revisit the assessment when the skill is updated.

## Reference(s):

- [Options and parameters](references/options.md)
- [Intent routing](references/routing.md)
- [Output contract](references/contract.md)
- [Errors and handling](references/errors.md)
- [Clarifying questions](references/ask.md)
- [FAQ and setup](references/faq.md)
- [Demand mining](references/demand-mining.md)
- [Customer acquisition](references/customer-acquisition.md)
- [Service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON results, with concise analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the query and the public data available from Douyin.]

## Skill Version(s):

1.5.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
