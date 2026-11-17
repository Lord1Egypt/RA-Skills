## Description:

Builds a curated Twitter industry watchlist of key voices using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, investors, executives, and industry professionals use this skill to discover, score, and organize high-signal Twitter/X accounts for industry monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify credentials may be exposed if tokens are placed in URLs, logs, or shared command histories.

Mitigation: Use a least-privilege APIFY_TOKEN, avoid verbose logging or sharing command histories, and prefer environment variables, MCP, or helper workflows over putting tokens in URLs.

Risk: The generated watchlist can include low-quality, promotional, bot-like, unavailable, or suspended accounts if scraper results are used without review.

Mitigation: Apply the skill's quality filters, review bot and promotional signals, and keep the final list small enough for practical monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/building-twitter-industry-watchlist)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with optional shell commands and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account handles, follower counts, engagement metrics, topic focus, influence scores, and Twitter/X list creation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
