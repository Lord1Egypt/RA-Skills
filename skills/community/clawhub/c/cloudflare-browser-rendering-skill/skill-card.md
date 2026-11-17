## Description:

Use Cloudflare Browser Rendering REST APIs to extract rendered webpage content as Markdown or crawl whole sites asynchronously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cytwyatt](https://clawhub.ai/user/cytwyatt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract content from JavaScript-rendered pages, crawl documentation or knowledge-base sites, and prepare rendered web content for summarization, search, monitoring, or RAG workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated rendering can expose passwords, production session cookies, bearer tokens, or sensitive HTML to Cloudflare through command-line arguments and API requests.

Mitigation: Avoid real credentials and production sessions; use least-privilege Cloudflare tokens, temporary test accounts, short-lived sessions, and narrowly scoped inputs when authenticated rendering is unavoidable.

Risk: Crawls can retrieve more pages than intended or generate excessive output when scope is too broad.

Mitigation: Start with small depth and limit values, avoid external links unless required, poll lightly, and save large crawl outputs to files instead of dumping them into chat.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cytwyatt/skills/cloudflare-browser-rendering-skill)
- [Project Homepage](https://github.com/cytwyatt/cloudflare-browser-rendering-skill)
- [Decision Guide](references/decision-guide.md)
- [/markdown Endpoint Notes](references/markdown-endpoint.md)
- [/crawl Endpoint Notes](references/crawl-endpoint.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON returned by command-line helpers, with optional saved JSON and Markdown files for crawl results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID environment variables.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
