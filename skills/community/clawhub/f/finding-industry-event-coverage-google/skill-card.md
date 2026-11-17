## Description:

Finds industry event and conference coverage on Google using apidojo's Google Search scraper and returns an article list with title, publication, date, coverage type, and key announcement signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Industry analysts, competitive intelligence teams, PR professionals, and event marketers use this skill to find and classify Google coverage of conferences, trade shows, summits, and related announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Apify URLs or command output may expose token values in logs or shared terminal output.

Mitigation: Use a narrowly scoped Apify token where possible, avoid sharing authenticated URLs, and prefer the helper script or MCP path over raw curl commands with token query parameters.

Risk: Event coverage search results can be incomplete, noisy, or stale when event names are ambiguous or coverage is sparse.

Mitigation: Try official and common event names, broaden search terms when result counts are low, remove entries with missing key fields, and report filtering assumptions in the summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-industry-event-coverage-google)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown table and summary with optional JSON or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes result classification and relevance scoring guidance; saved files are optional when the actor helper is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
