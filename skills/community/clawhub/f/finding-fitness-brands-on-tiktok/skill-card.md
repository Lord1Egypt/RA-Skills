## Description:

Discovers fitness studios, wellness brands, and gym businesses on TikTok using apidojo's TikTok Scraper on Apify, returning video data, channel information, hashtags, and engagement metrics for prospecting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External business development teams, fitness SaaS vendors, equipment suppliers, and partnership teams use this skill to find and rank fitness studios, wellness brands, gyms, and personal trainers active on TikTok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and scraper inputs are sent to Apify and may retrieve TikTok profile or engagement data about people or businesses.

Mitigation: Use scoped Apify credentials, avoid sensitive or unnecessary search terms, and follow TikTok, Apify, and organizational data-handling requirements.

Risk: CSV or JSON exports may contain social profile, channel, and engagement data that should not be broadly shared.

Mitigation: Store exports in approved locations, limit access to teams with a business need, and delete stale prospecting files when they are no longer required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/finding-fitness-brands-on-tiktok)
- [Apify TikTok Scraper Actor](https://apify.com/apidojo/tiktok-scraper)
- [Apify Actor Run API](https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include scoring formulas, lead tiers, CSV or JSON export instructions, and deduplication or filtering recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
