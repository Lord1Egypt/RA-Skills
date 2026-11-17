## Description:

Extract verified business email addresses from Google Maps listings and prepare contact lists for outreach campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmapsscraper](https://clawhub.ai/user/gmapsscraper)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales operators, and developers use this skill to define a business search target, run Google Maps email extraction through gmapsscraper.io, and filter the downloaded contacts for outreach readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied search text may be inserted into shell commands.

Mitigation: Review and sanitize industry and location values before running generated curl commands.

Risk: The workflow requires an external API key and produces exported contact CSVs.

Mitigation: Use a dedicated low-privilege API key and deliberately store, share, or delete downloaded CSV files.

Risk: Outreach requirements vary by target region and campaign context.

Mitigation: Independently verify applicable outreach-law requirements before using extracted contacts.

Risk: The skill includes cost and promotional guidance for the extraction service.

Mitigation: Confirm credit costs and service terms before authorizing paid or high-volume extraction.

## Reference(s):

- [Business Email Extractor on ClawHub](https://clawhub.ai/gmapsscraper/skills/business-email-extractor)
- [gmapsscraper.io](https://gmapsscraper.io)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples and CSV contact-list output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the GMAPS_SCRAPER_API_KEY environment variable; extraction results are downloaded as CSV for filtering.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
