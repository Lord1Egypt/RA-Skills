## Description:

Finds medical practices, clinics, dental offices, and healthcare providers through Google Search using apidojo's Google Search Scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

HealthTech vendors, medical suppliers, and B2B service teams use this skill to discover healthcare practices in target locations and build initial outreach prospect lists from Google results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Apify and may reflect business targeting plans.

Mitigation: Use only approved search terms and avoid including sensitive internal strategy, customer data, or regulated personal data in queries.

Risk: Running the skill requires an Apify API token or MCP connection.

Mitigation: Store credentials in approved secret management, limit token scope where possible, and avoid pasting tokens into prompts or shared logs.

Risk: Generated healthcare prospect lists are business data and may be subject to outreach or Google-derived-results obligations.

Mitigation: Review applicable compliance requirements before using the data for sales outreach or downstream enrichment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-healthcare-practices-via-google-search)
- [Apify Google Search Scraper run endpoint](https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON actor inputs; result data may be saved as CSV or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces healthcare prospect lists with practice names, website URLs, Google snippets, and optional ranking tiers when result data is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
