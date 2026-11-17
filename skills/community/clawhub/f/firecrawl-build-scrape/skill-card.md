## Description:

Integrate Firecrawl `/scrape` into product code for single-page extraction from a known URL, producing markdown, HTML, links, screenshots, metadata, or structured page output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add page-level Firecrawl `/scrape` integrations when an application already has a target URL and needs content for retrieval, summarization, enrichment, monitoring, or downstream indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using Firecrawl for scraping can send target URLs and retrieved page content to the hosted service or configured deployment.

Mitigation: Do not send private internal URLs, authenticated pages, secrets, regulated content, or other sensitive data through the hosted service unless the organization has approved that data handling.

Risk: Some privacy or data-boundary requirements may not be appropriate for hosted scraping.

Mitigation: Use a properly controlled self-hosted Firecrawl deployment when organizational privacy boundaries require it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/eohmig/skills/firecrawl-build-scrape)
- [Firecrawl homepage](https://www.firecrawl.dev)
- [Firecrawl Node / TypeScript source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/node)
- [Firecrawl Python source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/python)
- [Firecrawl Rust source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/rust)
- [Firecrawl Java source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/java)
- [Firecrawl Elixir source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/elixir)
- [Firecrawl cURL / REST source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/curl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with implementation notes, configuration details, and code or shell command examples as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIRECRAWL_API_KEY for hosted Firecrawl requests; FIRECRAWL_API_URL may be used for an approved self-hosted deployment.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
