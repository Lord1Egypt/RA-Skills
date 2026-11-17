## Description:

Enables agents to query ApocData's public A-share market API for quotes, financials, capital flows, technical factors, announcements, sectors, convertible bonds, macro data, and comprehensive stock analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjialegit](https://clawhub.ai/user/hanjialegit)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users, developers, and analysts use this skill to let an agent fetch and summarize China A-share market data for research workflows, including quote checks, fundamentals, fund flows, announcements, sector analysis, and macro context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some setup paths can run or install downloaded code without verification.

Mitigation: Install the reviewed artifact through a trusted channel when possible, or inspect downloaded archives and scripts and verify published checksums or signatures before placing files under ~/.claude/skills.

Risk: The optional MCP server path can execute a third-party package.

Mitigation: Pin and audit the MCP server package before enabling it in an agent environment.

Risk: Financial outputs can be affected by delayed, sparse, missing, or conflicting market data.

Mitigation: Show trade_date, as_of, updated_at, delayed_minutes, and freshness details; cross-check material claims; stop deterministic conclusions on abnormal data; and frame results as research rather than investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanjialegit/skills/apocdata-skill)
- [ApocData platform](https://www.apocdata.com)
- [ApocData OpenAPI specification](https://www.apocdata.com/api/blade-dataplatform/open/data/openapi.json)
- [Interface boundaries and known behaviors](artifact/references/boundaries.md)
- [Financial output safety rules](artifact/references/safety-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON API response summaries and inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data freshness, distinguish raw data from AI summaries and agent inferences, and avoid investment advice.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
