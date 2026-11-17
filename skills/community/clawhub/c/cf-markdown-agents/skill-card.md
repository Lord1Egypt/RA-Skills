## Description:

Fetch web content using Cloudflare's Markdown for Agents protocol. Automatically converts HTML to Markdown with 80% token reduction. Use when fetching web pages for AI processing, web scraping, content extraction, or when the user mentions "Markdown for Agents", "cf-markdown", or needs structured web content in Markdown format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinian5216](https://clawhub.ai/user/xinian5216)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fetch public web pages through Cloudflare Markdown for Agents and receive cleaner Markdown for AI processing, web research, scraping, and content extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch helper accepts arbitrary URLs and can reach non-web, local, private, or link-local resources.

Mitigation: Use it only for user-directed fetching of trusted public HTTPS pages, and add protocol, address-range, redirect, timeout, and response-size controls before broader deployment.

Risk: Fetched content and response headers may expose more information than the user intended to process or display.

Mitigation: Avoid printing unnecessary headers and review fetched Markdown before using it as agent input or downstream training/search material.

## Reference(s):

- [Markdown for Agents protocol reference](references/protocol.md)
- [Markdown for Agents examples](references/examples.md)
- [Cloudflare Markdown for Agents documentation](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/)
- [Cloudflare Markdown for Agents announcement](https://blog.cloudflare.com/markdown-for-agents/)
- [Content Signals Framework](https://contentsignals.org/)
- [ClawHub skill page](https://clawhub.ai/xinian5216/skills/cf-markdown-agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown and shell/code examples for fetching web content with Accept headers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fetched response headers and Markdown content; Cloudflare-enabled sites can report estimated Markdown token counts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
