## Description:

Extracts clean, LLM-optimized Markdown from one or more URLs, including JavaScript-rendered pages, using Firecrawl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill when they already have URLs and need Firecrawl commands to scrape web pages into Markdown or JSON for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows unpinned third-party CLI execution through npx, which can run code that has not been audited for this release.

Mitigation: Remove the npx allowance or pin Firecrawl to an audited exact version, and run scraping with limited filesystem, credential, and network exposure.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/skills/firecrawl-scrape-cn)
- [firecrawl-search](../firecrawl-search/SKILL.md)
- [firecrawl-browser](../firecrawl-browser/SKILL.md)
- [firecrawl-download](../firecrawl-download/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; Firecrawl commands may produce Markdown or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single or multiple URLs; scraped outputs are commonly saved under .firecrawl/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
