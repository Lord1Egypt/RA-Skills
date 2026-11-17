## Description:

Firecrawl Map helps agents discover and list URLs on a website, optionally filtering results with a search query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to map a known website, find specific pages on a domain, list site URLs, and prepare targeted scraping or crawling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx execution can run Firecrawl code that changed after this artifact was reviewed.

Mitigation: Use a reviewed local Firecrawl installation or a version-pinned CLI invocation before enabling the skill in sensitive environments.

## Reference(s):

- [Firecrawl Map ClawHub release page](https://clawhub.ai/eohmig/skills/firecrawl-map)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; Firecrawl commands can produce plain text or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports search filtering, URL limits, sitemap handling, subdomain inclusion, and optional output file paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
