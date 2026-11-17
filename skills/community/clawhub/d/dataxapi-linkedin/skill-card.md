## Description:

Retrieves public LinkedIn posts, company information, ads, and available video transcripts through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Users and analysts can retrieve public LinkedIn posts, company details, ad library listings, and available video transcripts by search terms, account name, ID, or link. The agent can use these results to answer questions about LinkedIn content and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms are sent to DataXAPI and may disclose confidential context.

Mitigation: Keep confidential context out of discovery queries; use only the public search terms or identifiers needed for the lookup.

Risk: API calls use prepaid balance, and additional pages can incur additional charges.

Mitigation: Check endpoint prices, set a spending limit, and cap calls or pages before retrieving results.

Risk: The CLI package and service-side behavior are not covered by the bundled instruction review.

Mitigation: Prefer REST or remote MCP, or review and pin the CLI version before installing it.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [LinkedIn API Reference](https://dataxapi.com/apis/linkedin/)
- [LinkedIn Pricing](https://dataxapi.com/pricing/linkedin/)
- [DataXAPI MCP Setup Guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured JSON results with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public LinkedIn data; search results may be incomplete, and returned content is third-party text.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
