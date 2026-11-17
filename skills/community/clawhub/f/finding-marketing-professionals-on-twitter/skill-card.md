## Description:

Finds marketing professionals and growth specialists to recruit using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Hiring managers, growth-stage companies, and recruiting firms use this skill to find marketing professionals and growth specialists on Twitter/X, enrich candidate profiles, score fit, and prepare recruiting shortlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recruiting search criteria and candidate handles are sent to Apify.

Mitigation: Use the skill only when sharing this data with Apify is intended, and avoid sending or retaining more candidate data than the recruiting task requires.

Risk: REST examples place the Apify token in URL query strings.

Mitigation: Prefer Apify MCP or API calls that keep the token in an Authorization header, and use a least-privilege token.

Risk: Unlimited or broad scraping can collect more profile data than needed.

Mitigation: Set explicit maxItems limits and review candidate data before storage or downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-marketing-professionals-on-twitter)
- [Apify tweet scraper API endpoint](https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN)
- [Apify Twitter user scraper API endpoint](https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown candidate tables with optional CSV or JSON files and inline shell/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate outputs may include handles, names, specialties, locations, follower counts, activity signals, scores, and bio highlights.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
