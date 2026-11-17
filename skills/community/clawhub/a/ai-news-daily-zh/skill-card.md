## Description:

Generates a Chinese executive-style daily AI news briefing by using Tavily and optional SearXNG search, then deduplicating, ranking, summarizing, and adding concise strategic insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davyzhou1977-sketch](https://clawhub.ai/user/davyzhou1977-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and operators use this skill to generate a same-day Chinese AI industry briefing with dated source links, concise summaries, and business-oriented insight. It is intended for daily manual use or scheduled OpenClaw runs when the required search tools and credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tavily search access and can optionally use a SearXNG endpoint.

Mitigation: Install only when those external search services are acceptable for the intended queries and operating environment.

Risk: The installation guidance includes a troubleshooting command that can print the Tavily API key.

Mitigation: Avoid commands that display secrets; verify credential presence without exposing the key value.

Risk: The scheduled-run script sets HTTP and HTTPS proxy variables to 127.0.0.1:7897.

Mitigation: Remove or explicitly configure the proxy unless the operator intentionally trusts that local service.

Risk: A remote SearXNG endpoint may be configured over plain HTTP.

Mitigation: Prefer HTTPS for remote SearXNG instances.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davyzhou1977-sketch/skills/ai-news-daily-zh)
- [Publisher profile](https://clawhub.ai/user/davyzhou1977-sketch)
- [Tavily](https://tavily.com)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Chinese Markdown briefing or Feishu card JSON containing Markdown body text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normally produces 5-9 dated AI news items with source links, short summaries, short insights, and a closing daily assessment.]

## Skill Version(s):

1.3.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
