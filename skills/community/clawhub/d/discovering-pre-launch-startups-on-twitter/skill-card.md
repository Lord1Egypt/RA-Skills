## Description:

Discovers pre-launch startups and products on Twitter using apidojo's Twitter Search scraper, returning startup handles, product descriptions, waitlist or launch signals, stage, and niche.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users such as VC scouts, accelerator teams, and competitive intelligence teams use this skill to search Twitter/X for early signals of pre-launch startups, beta products, waitlists, and founders building in public.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries and collection parameters to a third-party Apify/apidojo Twitter scraper.

Mitigation: Use the skill only when third-party scraping is acceptable, and avoid sensitive client or internal scouting terms in queries.

Risk: The documented REST fallback places an Apify token in the request URL.

Mitigation: Prefer authenticated tooling or authorization headers, and avoid token-in-URL usage where logs or browser history could expose credentials.

Risk: Unlimited or broad searches can collect more data than intended.

Mitigation: Set tight maxItems limits and use focused search filters before running the actor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/discovering-pre-launch-startups-on-twitter)
- [Apify tweet-scraper run API](https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN)
- [Apify actor run dataset items API](https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and optional JSON or CSV files from the Apify actor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include classified startup results, relevance scores, summary findings, and notes about removed low-quality records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
