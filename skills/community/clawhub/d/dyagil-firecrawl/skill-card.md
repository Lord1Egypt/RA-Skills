## Description:

Scrape, search, map, and crawl the web for AI agents via the Firecrawl API when basic HTTP fetching is not enough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve clean web content, search results with page content, URL maps, and documentation crawls through Firecrawl. It is most useful for JavaScript-heavy pages, SPA sites, and documentation sets where basic fetch tools return empty or noisy content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill on private, authenticated, login, or form pages can expose sensitive data to a third-party scraping provider.

Mitigation: Prefer public pages and documentation crawls; do not automate passwords, MFA codes, tokens, payment details, or other secrets unless the provider security and privacy posture has been reviewed and accepted.

Risk: Large crawls and maps can consume Firecrawl credits quickly.

Mitigation: Set explicit crawl or map limits, start with small test runs, and warn users about credit cost before broad crawls.

Risk: The skill relies on a Firecrawl API key stored on the local machine.

Mitigation: Store the API key with restrictive file permissions and keep it out of source control, logs, and generated artifacts.

## Reference(s):

- [Firecrawl documentation](https://docs.firecrawl.dev)
- [Firecrawl website](https://firecrawl.dev)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce file paths for saved markdown, HTML, JSON, URL lists, or crawled documentation output.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
