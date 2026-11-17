## Description:

Searches public Meta, Google, LinkedIn, TikTok, and Reddit ad libraries through ToolRouter to help analyze advertisers' ads and creative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blakefolgado](https://clawhub.ai/user/blakefolgado)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and researchers use this skill to compare competitors' public ads, identify recurring creative themes, and summarize ad copy, dates, platforms, and available transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad research requests are sent to the third-party ToolRouter service.

Mitigation: Avoid including sensitive business plans or private customer data in requests.

Risk: The optional Claude Code setup invokes an unpinned npm MCP package.

Mitigation: Review or pin the toolrouter-mcp package before using that setup path.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/blakefolgado/skills/ad-library-scraper)
- [ToolRouter ad library search](https://toolrouter.com/tools/ad-library-search)
- [ToolRouter setup guide](https://toolrouter.com/docs/markdown/quickstart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should state the country, status, and date range; spend and reach appear only when provided by the source library.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
