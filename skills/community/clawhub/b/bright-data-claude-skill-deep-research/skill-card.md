## Description: <br>
Provides web research workflows using Bright Data MCP tools for search, scraping, structured extraction, and browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to collect web data, compare competitors or prices, extract structured information, and synthesize market, academic, or product research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can click links, interact with pages, and maintain sessions, including on logged-in or private pages. <br>
Mitigation: Use the skill only on pages you own or are authorized to access, keep actions read-only by default, and require explicit approval before any interactive browser step. <br>
Risk: Queries, target URLs, and scraped page content may be sent to Bright Data and target websites. <br>
Mitigation: Avoid sensitive, private, or regulated data unless the user has approved that disclosure path and it fits the applicable data-handling policy. <br>
Risk: Large or broad scraping runs can exceed intended scope, rate limits, or site expectations. <br>
Mitigation: Set explicit domains, URL counts, collection modes, and rate limits before execution, and stop or narrow the run when failures, blocks, or unexpected content appear. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/liangdabiao/bright-data-claude-skill-deep-research) <br>
- [Analysis and Report Template](references/analysis-report.md) <br>
- [Content Scraping Template](references/content-scraping.md) <br>
- [Data Extraction Template](references/data-extraction.md) <br>
- [Deep Scraping Template](references/deep-scraping.md) <br>
- [Search Discovery Template](references/search-discovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON datasets, structured analyses, and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source references, methodology notes, extracted fields, and caveats about failed or incomplete scraping.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
