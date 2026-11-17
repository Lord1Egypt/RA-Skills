## Description:

Finds TikTok UGC creators for brand campaigns using apidojo's TikTok scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce brands, DTC companies, and influencer marketing managers use this skill to discover and score TikTok micro-creators for paid UGC campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens may be exposed through command history, logs, or URL query strings.

Mitigation: Prefer MCP or API calls that pass APIFY_TOKEN outside query strings, use a restricted token, and avoid logging commands that include credentials.

Risk: TikTok search terms, profile URLs, and exported creator rosters can reveal campaign strategy or personal data.

Mitigation: Avoid sensitive target lists, minimize shared inputs, and store exported creator rosters carefully.

Risk: Creator-fit scores can be misleading when a single viral post, inactive account, or low niche concentration skews metrics.

Mitigation: Calculate averages from recent posts, flag high-variance outliers, skip inactive creators, and check niche concentration before using a roster.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-tiktok-ugc-creators-for-brands)
- [Apidojo publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown creator roster with tables, scoring notes, and optional shell or API commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include creator handles, follower counts, average views, engagement rates, niche fit, content samples, and exported CSV or JSON guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
