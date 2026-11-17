## Description:

Generates B2B/B2C leads by scraping Google Maps, websites, Instagram, TikTok, Facebook, LinkedIn, YouTube, and Google Search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apify](https://clawhub.ai/user/apify)

### License/Terms of Use:


## Use Case:

Sales, growth, and marketing users use this skill to choose and run Apify Actors that collect publicly available lead data for prospecting, enrichment, and outreach preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search criteria and actor inputs to Apify.

Mitigation: Avoid confidential inputs and install only when the user is comfortable sharing the query and actor input data with Apify.

Risk: The skill handles scraped public contact data for lead generation.

Mitigation: Review platform terms, privacy obligations, and outreach requirements before using or exporting lead data.

Risk: CSV or JSON exports may contain sensitive contact data or spreadsheet-interpretable content.

Mitigation: Treat exports as sensitive files, avoid shared workspaces for outputs, and use caution when opening CSV files in spreadsheets.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/apify/skills/apify-lead-generation)
- [Apify](https://apify.com)
- [Apify Actor API](https://api.apify.com/v2/acts/:actorId)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and optional CSV or JSON lead exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN, node, and mcpc; exported CSV or JSON files are written under the current working directory when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
