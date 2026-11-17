## Description:

Builds production-ready web scrapers using Bright Data APIs, with guidance for site analysis, API selection, selector extraction, pagination, concurrency, validation, and runnable implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to build, test, and run Bright Data-backed scrapers for authorized web data workflows, including product pages, job listings, search results, paginated sites, and dynamic pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, request metadata, and fetched page content may be sent to Bright Data as a third-party provider.

Mitigation: Install and use the skill only for authorized scraping workflows, use scoped API keys, and avoid private, internal, authenticated, or regulated pages unless approved.

Risk: The skill can help build scrapers for broad or arbitrary targets without enough scoping or safety checks.

Mitigation: Define the target site, data fields, scope, volume, and output format before running collection, and review generated scraper behavior before scaling.

Risk: Bulk scraping jobs can amplify cost, compliance, and operational impact if concurrency or pagination is misconfigured.

Mitigation: Start with a 1-3 page validation run, cap concurrency with semaphores, add retries and progress tracking, and inspect extracted data before allowing large jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meirk-brd/skills/brightdata-scraper-builder)
- [Supported Domains](references/supported-domains.md)
- [Site Analysis Guide](references/site-analysis-guide.md)
- [Pagination Patterns](references/pagination-patterns.md)
- [Concurrency Guide](references/concurrency-guide.md)
- [Bright Data documentation index](https://docs.brightdata.com/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with runnable scraper code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scrapers should be reviewed and tested on a small sample before bulk execution; examples rely on Bright Data credentials supplied through environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
