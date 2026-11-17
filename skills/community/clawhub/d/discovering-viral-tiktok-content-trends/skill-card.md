## Description:

Discovers viral content trends and trending formats on TikTok using apidojo's TikTok scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External TikTok content creators, brand social teams, and video content strategists use this skill to research viral content formats in a niche and produce a trend brief with high-performing posts, hook patterns, engagement metrics, trend freshness, and recommended content angles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback places APIFY_TOKEN in a URL, which can expose the token in logs or process listings.

Mitigation: Prefer the Apify MCP or helper-script path; if REST is necessary, change it to send the token in an Authorization header, keep tokens narrowly scoped, avoid logging token-bearing commands, and rotate exposed tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/discovering-viral-tiktok-content-trends)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/tiktok-scraper](https://apify.com/apidojo/tiktok-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown trend report with tables, scoring notes, hook analysis, and recommended content angles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CSV or JSON file output when the helper-script path is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
