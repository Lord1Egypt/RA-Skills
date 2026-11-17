## Description:

Finds digital marketing agencies, creative studios, and web design firms via Google Search using apidojo's Google Search Scraper on Apify, returning agency names, website URLs, snippets, relevance scores, and priority tiers for prospecting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, SaaS vendors, white-label providers, and B2B service companies use this skill to build prospecting lists of digital marketing agencies by keyword and location, then rank and classify search results for outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and related run parameters are sent to Apify and may reveal prospecting strategy or sensitive targets.

Mitigation: Avoid sensitive queries, use an appropriate Apify account, and tell users that Apify receives submitted search parameters.

Risk: Actor runs require APIFY_TOKEN and may consume Apify credits, especially with broad searches or high page counts.

Mitigation: Set maxItems or maxPagesPerQuery before running large jobs and review expected volume.

Risk: customMapFunction can alter remote actor output and behavior when supplied to the Apify actor.

Mitigation: Disable it by default and only use reviewed transformation code from trusted sources.

Risk: Google Search results can include directories, duplicates, stale snippets, or non-agency domains.

Mitigation: Deduplicate by domain, filter known directory, news, education, and government domains, and review records before outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-digital-agencies-via-google-search)
- [Apify Google Search Scraper run endpoint](https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON input examples; result data may be saved as CSV or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results typically include agency name, website URL, Google snippet, relevance score, and prospect tier.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
