## Description:

Performs deep scraping of complex sites like YouTube using containerized Crawlee, extracting validated, ad-free transcripts and page content as JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opsun](https://clawhub.ai/user/opsun)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Deep Scraper to retrieve public content or YouTube transcripts from dynamic web pages for downstream LLM processing and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary target URLs could expose private services reachable from the container.

Mitigation: Run only against authorized public URLs and enforce URL allowlists, private-network blocking, and redirect validation before deployment.

Risk: Browser-based scraping may collect sensitive or non-public content if pointed at restricted pages.

Mitigation: Do not use the skill for password-protected pages or non-public personal information, and review outputs before downstream use.

Risk: Unpinned runtime dependencies and incomplete container build evidence can make behavior harder to reproduce.

Mitigation: Pin dependencies and use a complete pinned Docker build before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/opsun/skills/deep-scraper)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON emitted to stdout, with Markdown command guidance when usage instructions are provided]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handlers truncate scraped page content or transcripts to 10000-15000 characters.]

## Skill Version(s):

1.0.1 (source: server release evidence; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
