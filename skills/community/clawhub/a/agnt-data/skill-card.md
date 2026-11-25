## Description:

Unified data API for AI agents. One API key for LinkedIn, YouTube, TikTok, X, Instagram, Reddit, and Facebook, plus web scraping, SEO data, and hosted webhook receiving. Structured JSON, no infra to run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use the skill to retrieve structured social, web, and SEO data through one API, and to receive and process hosted webhook deliveries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook receive URLs are the only authentication, and incoming events are not signature-verified.

Mitigation: Treat each receive URL as a secret and verify event authenticity through another trusted channel before acting on consequential events.

Risk: The security scan was partial, covering 10 of 11 components, with a degraded tool-misuse check.

Mitigation: Review the unscanned component and complete a full security assessment before relying on the skill in production.

## Reference(s):

- [Social Data documentation](https://superagnt.com/r/ch-social-data-docs)
- [Scoped Social Data MCP server](https://mcp.superagnt.com/mcp/social-data)
- [Social Data ClawHub listing](https://clawhub.ai/superagnt/skills/social-data)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON data, Markdown page content, and setup and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.19 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
