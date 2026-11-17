## Description:

Finds law firms and legal practices via Google Search using apidojo's Google Search Scraper on Apify, returning firm names, website URLs, and Google snippets for sales outreach and prospecting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business development teams use this skill to discover law firms by specialty and location, then classify Google results into prospect tiers for outreach list-building. It is especially suited to LegalTech SaaS vendors and B2B service providers targeting law firms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms entered into the hosted scraper may be shared with Apify.

Mitigation: Avoid entering confidential or regulated information in search queries unless that sharing is approved for the intended workflow.

Risk: The hosted actor requires an APIFY_TOKEN when run through the REST API or hosted workflow.

Mitigation: Provide the token only when execution is intended, protect it as a credential, and follow local secret-handling practices.

Risk: The optional customMapFunction is user-supplied transformation logic for the scraper workflow.

Mitigation: Review customMapFunction contents before use and omit it when a standard result transformation is sufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/finding-law-firms-via-google-search)
- [Apify Google Search Scraper Run API](https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, plus optional JSON or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs typically include firm names, website URLs, Google snippets, prospect scores, and labels such as PRIME_PROSPECT, WARM_LEAD, or LOW_PRIORITY.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
