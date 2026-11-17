## Description:

Search Google Scholar for academic papers and scholarly results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Google Scholar search requests into Dataify Scraper API calls and receive concise scholarly search results. It supports query, cited-by, all-versions, date, language, result-count, and output-format controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests are sent through Dataify using the user's Dataify API token.

Mitigation: Install and use the skill only when sending scholarly-search requests through Dataify is acceptable, and keep the token in environment configuration rather than chat.

Risk: The published scope excludes patents, but the artifact supports patent and U.S. case-law modes.

Mitigation: Review patent and U.S. case-law requests before execution and keep ordinary use focused on Google Scholar paper search.

Risk: Large or multi-page searches may increase credit usage.

Mitigation: Confirm high-volume, multi-page, or cost-changing requests before execution and prefer the preview or dry-run flow for parameter review.

## Reference(s):

- [Dataify Google Scholar API Reference](references/google_scholar_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-scholar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, Markdown parameter tables, shell commands, and optional raw JSON or HTML responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Dataify API token and returns compact user-facing scholarly result summaries by default; raw JSON or HTML is returned only when explicitly requested.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
