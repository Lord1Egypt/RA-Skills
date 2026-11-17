## Description:

Discovers and ranks TikTok creators in a niche or topic using apidojo's TikTok scrapers on Apify, returning creator profiles, audience metrics, engagement indicators, and outreach-ready links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External influencer marketers, brand partnership teams, and talent managers use this skill to find, filter, rank, and prepare outreach lists of TikTok creators by niche, follower range, region, language, or hashtag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens can be exposed when passed in URL query strings or captured in logs.

Mitigation: Use a narrowly scoped Apify token and prefer an authorization header, MCP, or another secret-managed flow instead of URL query tokens.

Risk: Creator searches and exported CSV or JSON files can reveal sensitive campaign strategy or outreach targets.

Mitigation: Avoid sensitive campaign details in searches and delete exported creator data when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/discovering-tiktok-creators-by-niche)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Files, Guidance]

**Output Format:** [Markdown with ranked tables, outreach notes, inline shell commands, and optional CSV or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Apify actor inputs, follower and engagement filters, profile URLs, and saved creator datasets when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
