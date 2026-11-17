## Description:

Analyze local competitors from a Google Maps CSV export. Compare ratings, reviews, digital presence, and positioning. Find market gaps and opportunities without any API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmapsscraper](https://clawhub.ai/user/gmapsscraper)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and market analysts use this skill to turn a local-business CSV export into competitor rankings, market-gap analysis, and positioning recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a specific commercial data source when users do not already have a CSV.

Mitigation: Disclose the commercial sourcing path to users and allow equivalent CSV exports from other lawful data sources.

Risk: CSV inputs may include business contact fields such as email and address.

Mitigation: Use only data the user is authorized to analyze and omit personal, confidential, or unnecessary contact details.

Risk: Market recommendations can be misleading if the CSV is stale, incomplete, or geographically mismatched.

Mitigation: Ask users to confirm the data source, location, category, and freshness before relying on rankings or next steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmapsscraper/skills/competitor-analysis-local)
- [GMapsScraper homepage](https://gmapsscraper.io)
- [GMapsScraper pricing](https://gmapsscraper.io/#pricing)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Structured Markdown report with tables, summary metrics, rankings, gap analysis, and recommended next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided Google Maps CSV export; no API calls are required by the skill.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
