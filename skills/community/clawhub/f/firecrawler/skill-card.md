## Description:

Web scraping and crawling with Firecrawl API. Fetch webpage content as markdown, take screenshots, extract structured data, search the web, and crawl documentation sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve web pages as markdown, capture screenshots, extract structured data, search the web, and crawl or map documentation sites through the Firecrawl API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs, page content, extraction prompts, screenshots, and crawl results are processed by Firecrawl as a third-party service.

Mitigation: Use the skill only for data transfers approved for Firecrawl, and avoid private or authenticated sites unless that use is authorized.

Risk: The skill depends on a Firecrawl API key and an installed third-party Python package.

Mitigation: Protect FIRECRAWL_API_KEY, install the package in a virtual environment, and consider pinning the Firecrawl package version.

Risk: Crawls and screenshots can consume credits or write files to user-supplied paths.

Mitigation: Set crawl limits deliberately and review output paths before running commands.

## Reference(s):

- [Firecrawl](https://firecrawl.dev)
- [Firecrawl API Keys](https://www.firecrawl.dev/app/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, plain text, image files, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIRECRAWL_API_KEY and may write screenshots or crawled markdown files when an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
