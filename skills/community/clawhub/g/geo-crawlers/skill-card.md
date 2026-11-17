## Description:

AI crawler access analysis. Checks robots.txt, meta tags, and HTTP headers to determine which AI crawlers can access the site. Provides a complete access map and recommendations for maximizing AI visibility while maintaining appropriate control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and marketing teams use this skill to audit whether AI crawlers can access a website and to generate practical recommendations for AI search visibility and crawler control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawler recommendations may conflict with an organization's policy on AI search visibility, training-data access, or content reuse.

Mitigation: Review the generated recommendations against the organization's crawler, AI visibility, and training-data policies before changing robots.txt, headers, or page metadata.

Risk: The skill fetches public pages from the website selected for analysis and writes a local report.

Mitigation: Run it only for websites the user is authorized to audit, and review the generated GEO-CRAWLER-ACCESS.md report before sharing or acting on it.

## Reference(s):

- [OpenAI GPTBot](https://openai.com/gptbot)
- [OpenAI crawler overview](https://docs.openai.com/bots/overview)
- [OpenAI ChatGPT-User bot](https://openai.com/bot)
- [Anthropic ClaudeBot](https://www.anthropic.com/claude-bot)
- [PerplexityBot](https://perplexity.ai/perplexitybot)
- [Amazonbot](https://developer.amazon.com/support/amazonbot)
- [Common Crawl FAQ](https://commoncrawl.org/faq/)
- [Content Signals](https://contentsignals.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with crawler access tables, findings, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local GEO-CRAWLER-ACCESS.md report when used as directed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
