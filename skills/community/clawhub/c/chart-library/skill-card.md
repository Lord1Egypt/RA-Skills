## Description:

Chart Library helps agents find historically similar stock chart patterns and summarize forward-return outcomes from Chart Library API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grahammccain](https://clawhub.ai/user/grahammccain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-research agents use this skill to search visual stock-chart analogs, compare historical follow-through returns, and present plain-English pattern summaries. Outputs should be treated as historical research, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart queries, optional screenshots, and configured API keys may be sent to chartlibrary.io.

Mitigation: Review data-sharing expectations before use and prefer runtimes that restrict outbound network access to documented Chart Library endpoints.

Risk: Historical pattern outcomes may be mistaken for financial advice or predictions.

Mitigation: Frame outputs as historical research, include uncertainty and sample-size context, and avoid predictive language.

## Reference(s):

- [Chart Library homepage](https://chartlibrary.io)
- [Chart Library OpenAPI spec](https://chartlibrary.io/api/openapi.json)
- [Chart Library AI plugin manifest](https://chartlibrary.io/.well-known/ai-plugin.json)
- [Chart Library MCP server](https://github.com/grahammccain/chart-library-mcp)
- [ClawHub skill page](https://clawhub.ai/grahammccain/skills/chart-library)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text summaries with structured chart-pattern metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include match counts, outcome distributions, median returns, ranges, and API-derived summaries.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
