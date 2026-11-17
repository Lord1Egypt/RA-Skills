## Description:

Use Crawl4AI for web scraping and content extraction, including structured data extraction, Markdown conversion, batch crawling, and AI-driven web data collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and run Crawl4AI for web scraping, content-to-Markdown conversion, structured JSON extraction, batch crawling, deep crawling, and optional LLM-assisted extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawler and browser tooling can access broad network targets, persistent browser profiles, downloads, and cached page content.

Mitigation: Use an isolated environment, avoid private or authenticated sites unless explicitly intended, avoid normal browser profiles, and keep downloads and caches in disposable directories.

Risk: Unpinned package and Docker image installation can change behavior across releases.

Mitigation: Pin the Crawl4AI package version and Docker image digest before use.

Risk: Remote LLM extraction can disclose crawled page content to the configured provider.

Mitigation: Use remote LLM extraction only for content approved for that provider, or use a local model when page content should remain local.

## Reference(s):

- [Crawl4AI API Reference](references/api-reference.md)
- [Crawl4AI GitHub Repository](https://github.com/unclecode/crawl4ai)
- [Crawl4AI Documentation](https://docs.crawl4ai.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Crawl4AI installation commands, crawler configuration, API usage examples, and safety scoping guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
