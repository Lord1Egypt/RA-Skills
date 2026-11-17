## Description:

Finds podcast hosts for PR and guest outreach using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External PR teams, executives, authors, founders, and media relations users use this skill to find and prioritize podcast hosts for guest outreach in a specific topic or industry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, handles, and public Twitter/X-derived data are sent to Apify under the user's APIFY_TOKEN.

Mitigation: Protect the APIFY_TOKEN, review Apify data handling requirements, and use conservative maxItems limits.

Risk: Results may include listeners, content-sharing accounts, inactive hosts, or shows that are not realistic outreach targets.

Mitigation: Verify that profiles identify the person as a host, check recent episode activity, and review premium or large-media placements before outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-podcast-hosts-for-outreach)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify tweet scraper API endpoint](https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with tables, shell commands, JSON examples, and optional CSV or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs podcast host handles, show names, topic focus, follower counts, activity signals, outreach scores, and personalization guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
