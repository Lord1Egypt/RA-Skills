## Description:

Company firmographics, tech stack, headcount, and intelligence from a domain — agent-ready account research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, revenue operations, and market research teams can use this skill to enrich company domains or names, filter lists against an ideal customer profile, build prospect lists, and map markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company domains, names, and enrichment requests are sent to Superagnt's external API, authenticated with an API key.

Mitigation: Only submit company information you are authorized to share, and keep SUPERAGNT_API_KEY in the environment rather than placing it in prompts or command text.

## Reference(s):

- [Company Enrichment documentation](https://superagnt.com/r/ch-company-enrichment-docs)
- [Scoped Company Enrichment MCP server](https://mcp.superagnt.com/mcp/company-enrichment)
- [ClawHub listing](https://clawhub.ai/superagnt/skills/company-enrichment)

## Skill Output:

**Output Type(s):** [JSON, Company intelligence]

**Output Format:** [Structured company records, including firmographics, headcount, funding, competitors, technographics, and domain email data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports individual enrichment, search, discovery, and bulk enrichment; requires a SUPERAGNT_API_KEY for the documented curl workflow.]

## Skill Version(s):

2.0.14 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
