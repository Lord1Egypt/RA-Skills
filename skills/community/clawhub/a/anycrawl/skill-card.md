## Description:

Perform high-performance web scraping, crawling, and Google search with multi-engine support and structured data extraction via the AnyCrawl API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techlaai](https://clawhub.ai/user/techlaai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call AnyCrawl for web search, single-page scraping, asynchronous site crawling, crawl status checks, result retrieval, cancellation, and combined search-and-scrape workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends crawl targets, scraped URLs, search queries, and extraction options to a third-party API.

Mitigation: Use it only for URLs and query content approved for external transfer, and avoid private or internal targets unless that transfer is authorized.

Risk: Credential handling is under-disclosed and setup examples place API keys in shell profile files.

Mitigation: Use a limited-scope AnyCrawl key and avoid storing secrets in shared, synced, or broadly readable shell profile files.

Risk: Evidence.security reports a request-building bug affecting crawl status, results, and cancellation when tool arguments are untrusted.

Mitigation: Fix the request-building issue before relying on those crawl operations with untrusted arguments.

## Reference(s):

- [ClawHub AnyCrawl Skill Page](https://clawhub.ai/techlaai/skills/anycrawl)
- [AnyCrawl API Documentation](https://docs.anycrawl.dev)
- [AnyCrawl API Key Portal](https://anycrawl.dev)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [JSON API responses containing search results, scraped page content, crawl job metadata, crawl results, or error messages; documentation examples use Markdown with JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ANYCRAWL_API_KEY environment variable and sends requested URLs, search queries, and crawl options to the AnyCrawl API.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
