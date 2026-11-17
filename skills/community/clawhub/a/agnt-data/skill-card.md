## Description:

Unified data API for AI agents. One API key for LinkedIn, YouTube, TikTok, X, Instagram, Reddit, and Facebook, plus web scraping, SEO data, and hosted webhook receiving. Structured JSON, no infra to run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to retrieve structured social, web, and SEO data across supported platforms, and to receive and process hosted webhook events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service receives the API key and data sent through its API.

Mitigation: Install only if you trust the service, and protect the API key as a credential.

Risk: Incoming webhook payloads are accepted without vendor signature verification and may be untrusted.

Mitigation: Independently verify consequential events before acting on them; treat the receive URL as a secret.

Risk: The security scan covered 10 of 11 components and one analyzer was degraded, leaving incomplete evidence.

Mitigation: Review the skill and its behavior before installing or deploying it.

## Reference(s):

- [Social Data documentation](https://superagnt.com/r/ch-social-data-docs)
- [Social Data MCP server](https://mcp.superagnt.com/mcp/social-data)
- [Facebook API reference](references/facebook/README.md)
- [Instagram API reference](references/instagram/README.md)
- [LinkedIn API reference](references/linkedin/README.md)
- [Reddit API reference](references/reddit/README.md)
- [SEO API reference](references/seo/README.md)
- [TikTok API reference](references/tiktok/README.md)
- [Web API reference](references/web/README.md)
- [X API reference](references/x/README.md)
- [YouTube API reference](references/youtube/README.md)

## Skill Output:

**Output Type(s):** [JSON data, Markdown]

**Output Format:** [Structured JSON API results and scraped page content as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected platform endpoint and the user's service access.]

## Skill Version(s):

2.0.14 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
