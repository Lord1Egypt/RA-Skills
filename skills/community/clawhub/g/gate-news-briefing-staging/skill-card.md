## Description:

Generates recent crypto news briefings by retrieving Gate News events, trending headlines, and social sentiment, then deduplicating and organizing them into a concise markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce crypto market news briefings for general or coin-specific headline requests. It is intended for news summarization, event ranking, source-attributed reporting, and sentiment context, not technical analysis or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings depend on the availability and coverage of the Gate News MCP server.

Mitigation: Confirm Gate News MCP tools are available before use, label degraded sections when a feed fails, and avoid fabricating missing news or sentiment.

Risk: News and sentiment coverage may be biased toward available public crypto sources, including English-language sources.

Mitigation: Treat the output as a source-attributed news briefing, request broader sources when needed, and avoid using the summary as investment advice.

## Reference(s):

- [Gate News Briefing Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [Gate News Briefing MCP Specification](references/mcp.md)
- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-news-briefing-staging)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown briefing with sections for major events, trending news, social sentiment, and watch items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate News MCP data, preserves source attribution when available, labels the covered time range, and degrades gracefully when individual feeds are unavailable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
