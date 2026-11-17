## Description:

Finds real estate agents, brokers, property investors, and related professionals on Twitter/X using apidojo's Twitter User Scraper on Apify, returning profile details and lead-scoring guidance for outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, PropTech vendors, mortgage product teams, and B2B service providers use this skill to discover and prioritize real estate professionals on Twitter/X for outreach. It helps configure Apify Twitter user scraping, inspect profile fields, and rank potential leads using bio, follower, and website signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collecting public Twitter/X profile data for lead discovery can raise privacy, consent, and scope concerns.

Mitigation: Use the workflow only for appropriate public-profile lead discovery, set a clear maxItems limit, and keep collection aligned with the intended outreach purpose.

Risk: Follower, following, or retweeter collection can broaden data collection beyond the core user-search task.

Mitigation: Keep getFollowers, getFollowing, and getRetweeters disabled unless that expanded collection is specifically needed and approved.

Risk: A customMapFunction can transform output in ways reviewers may not expect.

Mitigation: Use customMapFunction only after reviewing the exact JavaScript transformation that will run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-real-estate-professionals-on-twitter)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify Twitter User Scraper API endpoint](https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, JSON input examples, and scoring guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide CSV or JSON exports when the Apify actor is executed.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
