## Description:

DuckDuckGo HTML search scraper CLI with JSON, CSV, OpenSearch, markdown, and compact outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camohiddendj](https://clawhub.ai/user/camohiddendj)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run DuckDuckGo searches from the command line and choose output formats suited for LLM context, structured processing, spreadsheets, documents, or OpenSearch feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata depends on the current npm release of ddg-search rather than a reviewed pinned version.

Mitigation: Use a least-privilege environment and pin the npm package version when stronger supply-chain control is required.

Risk: DuckDuckGo bot detection may stop scraping early and return only the results collected so far.

Mitigation: Treat search results as potentially partial and verify important findings against source pages before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camohiddendj/skills/ddg-search-cli)
- [ddg-search project homepage](https://github.com/camohiddendj/ddg-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output may be JSON, JSONL, CSV, Markdown, compact text, or OpenSearch XML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are written to stdout and progress to stderr; page, result-count, region, and time filters can constrain searches.]

## Skill Version(s):

2026.2.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
