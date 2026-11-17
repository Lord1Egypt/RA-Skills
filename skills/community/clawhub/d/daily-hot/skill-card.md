## Description:

Aggregates hot trends, news feeds, rankings, RSS content, and selected website content through the XiaoBenYang MCP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to fetch and summarize current trending topics, rankings, news items, RSS content, and website content from supported sources. It is suited for news monitoring, social trend discovery, technology updates, and related content aggregation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed through the generated .env file or a shared workspace.

Mitigation: Avoid committing or sharing .env files and rotate the XiaoBenYang API key if the workspace may have been exposed.

Risk: The upstream base URL can be redirected through XBY_GAOKAO_BASE_URL.

Mitigation: Verify that XBY_GAOKAO_BASE_URL is unset or points only to the expected trusted host before use.

Risk: The skill includes broad fetching capabilities, including website crawling.

Mitigation: Review the skill before installing and use it only in a trusted workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/daily-hot)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API base URL](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration guidance]

**Output Format:** [Markdown summaries of upstream JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; selected tools accept category, limit, ranking, or URL parameters.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
