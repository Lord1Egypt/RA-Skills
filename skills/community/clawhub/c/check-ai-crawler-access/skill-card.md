## Description:

Check which search and AI crawlers (GPTBot, ClaudeBot, PerplexityBot, CCBot, Google-Extended and more) a website's robots.txt allows. Use when someone asks why an AI assistant cannot see or cite a site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mitchkj25](https://clawhub.ai/user/mitchkj25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and people diagnosing crawler visibility can use this skill to check which search and AI crawlers a site's robots.txt allows and identify the rule that controls each result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A submitted site URL or optional page path may reveal private hostnames or sensitive paths to an external service.

Mitigation: Avoid submitting URLs or paths that contain private hostnames, sensitive page paths, or credentials.

## Reference(s):

- [Server-resolved source repository](https://github.com/mitchkj25/why-wont-ai/tree/main/skills/check-ai-crawler-access)
- [Why Won't AI MCP server](https://mcp.whywontai.com/)
- [Browser-based AI crawler robots.txt checker](https://whywontai.com/ai-crawler-robots-txt-checker)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crawler allow/block findings with the robots.txt rule that governs each result; an allow does not establish that the page is accessible to a crawler.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
