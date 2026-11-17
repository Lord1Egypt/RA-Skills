## Description:

Analyzes a competitor's YouTube channel content strategy and performance using apidojo's YouTube scraper on Apify, returning cadence, format mix, top topics, benchmarks, and engagement analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketing teams, YouTube strategists, and brand video teams use this skill to analyze competitor channels, compare content patterns, and identify topics, formats, lengths, and publishing cadences associated with stronger performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback places APIFY_TOKEN in the request URL, which can expose the token through shell history, logs, proxies, or shared terminals.

Mitigation: Prefer Apify MCP or a helper that sends the token in an Authorization header; use a narrowly scoped token and rotate it if the URL-token command has already been run in a logged or shared environment.

Risk: Strategy recommendations can be misleading when scraped channel data is incomplete, unusually small, skewed by a viral outlier, or missing subscriber counts.

Mitigation: Report sample size and data gaps, use median alongside mean, flag outliers, and validate findings before using them for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/analyzing-competitor-youtube-content-strategy)
- [Apify actor: apidojo/youtube-scraper](https://apify.com/apidojo/youtube-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown strategy report with tables, metrics, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CSV or JSON file outputs when the Apify helper is used with an output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
