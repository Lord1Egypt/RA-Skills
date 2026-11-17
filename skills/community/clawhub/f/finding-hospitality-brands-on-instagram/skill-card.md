## Description:

Discovers hotels, travel brands, resorts, and hospitality businesses on Instagram using apidojo's Instagram Scraper on Apify, returning account handles, follower counts, bios, and post engagement data for prospecting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External B2B sales and marketing teams use this skill to discover and prioritize hospitality prospects on Instagram, including hotels, resorts, tour operators, and travel brands, using account metadata and engagement signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram URLs and scrape parameters are sent to Apify and may reveal sensitive prospecting targets.

Mitigation: Confirm the target list is appropriate to send to Apify and avoid unnecessary sensitive targets.

Risk: APIFY_TOKEN exposure could allow unauthorized actor runs or account access.

Mitigation: Store APIFY_TOKEN as a secret and avoid pasting it into shared logs, prompts, or exported files.

Risk: CSV or JSON exports may contain account metadata and engagement data that require controlled handling.

Mitigation: Store exports according to the organization's privacy, retention, and compliance obligations.

Risk: Broad Instagram searches may include bloggers, aggregators, or consumer posts instead of target hospitality brands.

Mitigation: Apply the documented filters for bio terms, location tags, follower count, and aggregator domain checks before outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-hospitality-brands-on-instagram)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify Instagram Scraper REST API endpoint](https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON or CSV result options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide agents to run Apify actor calls and rank resulting Instagram accounts by follower count, engagement rate, and location tags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
