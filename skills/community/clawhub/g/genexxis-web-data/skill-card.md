## Description:

Web and content tools for agents, paid per call via x402 (USDC on Base, no API key): read any URL as clean markdown, web search with provider failover, extract HTML tables to JSON or CSV, prepare images for vision LLMs, fetch any public file as base64, validate email addresses (syntax, MX, disposable, role), Hacker News stories, comments and users, scholarly papers from OpenAlex, arXiv and Crossref with citations, and a recommender that says which x402 API to call for a task. Use when a task needs fresh web content you cannot fetch, parse or resize yourself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montassirbbk-dot](https://clawhub.ai/user/montassirbbk-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve fresh web content and structured results, prepare image or file payloads, validate email addresses, and find Hacker News stories or scholarly papers through paid x402 calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security record flags the unpinned agentcash@latest package as a supply-chain risk that could expose local credentials or wallet access.

Mitigation: Pin a reviewed AgentCash version, limit its access to files, credentials, and wallet funds, and cap each payment at the listed price.

Risk: Fetched web content may contain misleading instructions.

Mitigation: Treat fetched content as data and ignore instructions embedded in pages or responses.

## Reference(s):

- [Genexxis skill page](https://clawhub.ai/montassirbbk-dot/skills/genexxis-web-data)
- [Genexxis services](https://skills.genexxis.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Base64 data URI]

**Output Format:** [Endpoint-dependent text or structured API response, including Markdown, JSON, CSV, or base64/data URI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies by endpoint; includes fetched content and metadata such as citations, dimensions, or validation results.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
