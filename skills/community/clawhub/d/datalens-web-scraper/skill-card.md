## Description:

Use DataLens MCP tools to scrape structured data from any website open in Chrome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weird94](https://clawhub.ai/user/weird94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to guide structured scraping of lists, tables, comments, products, reviews, and other repeated webpage data through DataLens browser tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process authenticated browser pages and may expose sensitive or regulated data during scraping.

Mitigation: Use it only on pages the user is allowed to scrape, and avoid secrets or regulated/internal data unless approved.

Risk: The skill relies on unpinned npm tooling for DataLens commands.

Mitigation: Prefer a pinned and vetted DataLens package version before installing or running the tooling.

Risk: Scraped results and debug logs may be saved locally.

Mitigation: Clean up exported data and debug logs after use, especially when scraping private or authenticated pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weird94/skills/datalens-web-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create local JSON, CSV, or XLSX export files when scraping jobs are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
