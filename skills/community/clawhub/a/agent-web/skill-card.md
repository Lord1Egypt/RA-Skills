## Description:

Fetch public static HTML web pages and return clean, LLM-ready markdown while respecting robots.txt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foomworks](https://clawhub.ai/user/foomworks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external agents use Agent Web to fetch readable content from public static web pages as clean markdown for summarization, extraction, documentation review, or LLM context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs and fetched page content are sent to a disclosed third-party service.

Mitigation: Use the skill only for public, non-confidential, unauthenticated pages that the user is authorized to fetch.

Risk: The service is limited to static HTML and may refuse pages blocked by robots.txt, private network protections, redirects, size caps, or timeouts.

Mitigation: Treat refused or incomplete reads as expected limitations and use a different approved source path for JavaScript-rendered pages, PDFs, private pages, or access-controlled content.

## Reference(s):

- [Agent Web ClawHub Listing](https://clawhub.ai/foomworks/skills/agent-web)
- [Agent Web Service Homepage](https://agent-web.foomworks.workers.dev)
- [Agent Web MCP Endpoint](https://agent-web.foomworks.workers.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with REST and MCP examples; service responses contain JSON fields for title, word count, and markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for REST examples; MCP clients can call the remote tools directly.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
