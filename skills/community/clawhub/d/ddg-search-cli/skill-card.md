## Description: <br>
DuckDuckGo HTML search scraper CLI with JSON, CSV, OpenSearch, markdown, and compact outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camohiddendj](https://clawhub.ai/user/camohiddendj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run DuckDuckGo searches from the command line and capture results in structured or human-readable formats for downstream analysis, documents, or LLM context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing and trusting the ddg-search npm package and any install-time behavior it performs. <br>
Mitigation: Install only after reviewing the package source and supply-chain trust posture; use npm options such as disabling lifecycle scripts when install scripts are not desired. <br>
Risk: Unbounded or broad web searches can create excessive scraping activity or return partial results if DuckDuckGo triggers bot detection. <br>
Mitigation: Use bounded page or result limits for routine searches and treat early-stopped results as incomplete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/camohiddendj/ddg-search-cli) <br>
- [Project Homepage](https://github.com/camohiddendj/ddg-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples and structured output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports json, jsonl, csv, opensearch, markdown, and compact CLI result formats.] <br>

## Skill Version(s): <br>
2026.2.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
