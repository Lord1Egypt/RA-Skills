## Description:

Instructional knowledge that teaches an AI agent when and how to use Firecrawl to scrape, crawl, map, search, cite sources, control cost, handle errors, and extract structured web data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and operate Firecrawl workflows for web scraping, site crawling, URL mapping, search-backed retrieval, citation, and structured extraction. It is most useful when an agent already has access to Firecrawl through MCP tools or direct HTTP calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs, search queries, and scraped content may be sent to a third-party Firecrawl service.

Mitigation: Do not use the skill for secrets, internal hosts, private pages, personal data, or regulated content unless authorization and a compliance basis are established.

Risk: Firecrawl API keys could be exposed if copied into prompts, logs, examples, or generated files.

Mitigation: Keep FIRECRAWL_API_KEY in the environment only and reference it by variable name in commands and configuration.

Risk: Unbounded crawl, map, or search operations can waste credits or retrieve excessive content.

Mitigation: Set limits, scope paths, minimize requested formats, prefer cheaper operations, and monitor creditsUsed in responses.

Risk: Scraped, crawled, or searched pages can contain prompt injection or misleading claims.

Mitigation: Treat retrieved content as untrusted data, ignore embedded instructions, cite source URLs, and corroborate important claims.

Risk: Server-side scraping can target internal, loopback, metadata, private, or otherwise unauthorized URLs.

Mitigation: Avoid internal or sensitive targets by default and require a legitimate, explicit reason before scraping them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/skills/firecrawl-api-al)
- [Firecrawl documentation](https://docs.firecrawl.dev)
- [Firecrawl website](https://firecrawl.dev)
- [Endpoint reference](reference/endpoints.md)
- [Safety and security reference](reference/safety-and-security.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, curl examples, citations, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; assumes Firecrawl tools or API access are configured separately.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
