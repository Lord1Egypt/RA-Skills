## Description:

Analyzes competitor YouTube channel strategy and content performance using Apidojo's YouTube scraper, returning content mix, format performance, publishing cadence, engagement benchmarks, and strategic insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External YouTube content strategists, brand video teams, and competitive intelligence analysts use this skill to benchmark competitor channels, identify content and cadence patterns, and summarize engagement signals into strategic recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested YouTube channel, handle, keyword, or search data to Apify for scraping.

Mitigation: Use only data that is appropriate to process through Apify and review third-party service requirements before deployment.

Risk: Apify credentials can be exposed if token-bearing URLs or command output are copied into logs or shared transcripts.

Mitigation: Prefer authorization headers, avoid pasting token-bearing URLs into logs, and use a narrowly scoped Apify token where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/analyzing-youtube-competitor-channel-strategy)
- [Apify actor: apidojo/youtube-scraper](https://apify.com/apidojo/youtube-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables and optional shell or API command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save scraped result sets as CSV or JSON when the helper workflow is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
