## Description:

Crawl websites using Cloudflare Browser Rendering /crawl API. Async multi-page crawl with markdown/HTML/JSON output, link following, pattern filtering, and AI-powered structured data extraction. Use when crawling entire sites or multiple pages, building knowledge bases, extracting structured data from websites, or when web_fetch is insufficient (JS rendering, multi-page, authenticated crawls).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill492](https://clawhub.ai/user/bill492)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start and poll Cloudflare Browser Rendering crawl jobs for multi-page site crawling, knowledge-base collection, JavaScript-rendered pages, authenticated crawls, and structured data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes the local Cloudflare credential file as shell code.

Mitigation: Store the credential file in a tightly protected location, keep it writable only by trusted users, and do not generate or modify it from untrusted input.

Risk: The skill requires a Cloudflare token with Browser Rendering read and edit access.

Mitigation: Use a dedicated least-privilege token and rotate or revoke it if the credential file may have been exposed.

Risk: Crawl targets, page contents, prompts, schemas, and results are sent to Cloudflare services.

Mitigation: Avoid crawling sensitive or regulated content unless Cloudflare's data handling is acceptable for that data.

## Reference(s):

- [Cloudflare /crawl API Reference](references/api-reference.md)
- [ClawHub cf-crawl skill page](https://clawhub.ai/bill492/skills/cf-crawl)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Markdown, HTML, JSON]

**Output Format:** [Markdown guidance with bash commands and Cloudflare crawl results in markdown, HTML, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write full crawl results to a file, print raw API responses, or return summarized job and page metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
