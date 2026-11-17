## Description:

Searches recent A-share market news from market.ft.tech by semantic query and returns related news results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to route semantic news-search requests to market.ft.tech and present recent A-share related news with source sites and article links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and time filters are sent to market.ft.tech.

Mitigation: Install and use the skill only where sharing those news-search inputs with market.ft.tech is acceptable.

Risk: Instructions and expected output are Chinese-language, and date filters use Beijing-time handling.

Mitigation: Confirm users can interpret the Chinese result fields and normalize requested time windows to UTC+8 when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shawn92/skills/ftshare-news-data)
- [market.ft.tech](https://market.ft.tech)
- [Semantic Search News Endpoint](https://market.ft.tech/data/api/v1/market/data/semantic-search-news)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON from the helper script, typically summarized as Markdown or text with article sources and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a query; optional limit, year, start_time, and end_time filters narrow the returned news results.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
