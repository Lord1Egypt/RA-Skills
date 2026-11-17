## Description:

Finds fast-growing YouTube channels in a niche using apidojo's YouTube scraper and returns channel names, subscriber counts, growth signals, view momentum, upload frequency, and growth tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Brand partnership managers, talent scouts, sponsorship teams, and market analysts use this skill to discover YouTube creators with early growth momentum in a topic or niche.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback can expose an Apify API token in URLs that may be captured by command history, proxy logs, or audit logs.

Mitigation: Prefer the MCP or helper-script path, keep tokens in environment variables, use narrowly scoped tokens, and avoid pasting real tokens into REST curl examples.

Risk: YouTube search inputs and scraper results are sent through Apify/apidojo.

Mitigation: Install and run the skill only when that data flow is acceptable for the research task.

Risk: Growth tiers are analyst heuristics rather than guaranteed computed metrics.

Mitigation: Validate conclusions against the returned channel metrics before making partnership or sponsorship decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-youtube-channels-by-growth-rate)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify youtube-scraper actor](https://apify.com/apidojo/youtube-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, summary text, and optional shell commands or JSON/CSV file output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save scraper results as CSV or JSON when run through the helper-script path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
