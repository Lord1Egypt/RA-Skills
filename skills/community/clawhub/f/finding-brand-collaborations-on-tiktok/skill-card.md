## Description:

Discovers brand collaboration patterns and sponsored content on TikTok using apidojo's TikTok scrapers on Apify, returning creator handles, brand names, post performance, estimated reach, and collaboration frequency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External influencer marketing teams, competitive intelligence analysts, and brand partnership managers use this skill to find TikTok creator-brand partnerships, identify active campaigns in a category, and benchmark sponsored-content performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok search terms and collected public TikTok data are sent to Apify/apidojo.

Mitigation: Use the skill only for appropriate public-data research and avoid regulated, secret, or sensitive terms in search inputs.

Risk: The REST fallback places APIFY_TOKEN in a URL, which can expose the token through logs or command history.

Mitigation: Prefer the MCP or helper flow with credentials handled through environment variables, and avoid the REST fallback unless logging exposure is controlled.

Risk: Sponsored-content signals can be sparse, inconsistent, or ambiguous.

Mitigation: Review captions, brand mentions, creator bios, and post context before treating a detected creator-brand pair as confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-brand-collaborations-on-tiktok)
- [apidojo publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/tiktok-scraper](https://apify.com/apidojo/tiktok-scraper)
- [Apify actor: apidojo/tiktok-profile-scraper](https://apify.com/apidojo/tiktok-profile-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Apify results as CSV or JSON when the helper flow is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
