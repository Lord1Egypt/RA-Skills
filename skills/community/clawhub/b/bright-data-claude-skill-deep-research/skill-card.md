## Description:

This skill provides Bright Data MCP workflows for web research, scraping, structured extraction, market research, competitive analysis, price monitoring, and browser-assisted content collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdabiao](https://clawhub.ai/user/liangdabiao)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan and run Bright Data-powered web research workflows that discover sources, collect page content, extract structured data, and synthesize reports for market research, competitive intelligence, price comparison, academic research, and product analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automated scraping can collect data from sites or contexts where scraping is not permitted.

Mitigation: Use the skill only for authorized targets, review site terms and robots.txt, and keep collection rates conservative.

Risk: Submitted URLs and extracted page content may be handled by Bright Data or other external provider infrastructure.

Mitigation: Avoid private, logged-in, internal, regulated, or personal-data sources unless explicit authorization and data-handling approval are in place.

Risk: Browser automation and logged-in sessions can expose sensitive account state or access content beyond the intended scope.

Mitigation: Use dedicated, authorized sessions for approved targets only, avoid sensitive accounts, and close browser sessions after the task.

Risk: Scraped source content can be incomplete, blocked, stale, or misleading.

Mitigation: Cross-check important findings across sources, cite sources in reports, and preserve methodology and validation notes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liangdabiao/skills/bright-data-claude-skill-deep-research)
- [Search Discovery Template](references/search-discovery.md)
- [Content Scraping Template](references/content-scraping.md)
- [Data Extraction Template](references/data-extraction.md)
- [Deep Scraping Template](references/deep-scraping.md)
- [Analysis and Report Template](references/analysis-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown reports, structured JSON, source lists, extraction schemas, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include source references, methodology notes, extracted fields, validation notes, and recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
