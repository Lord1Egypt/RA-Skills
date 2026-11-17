## Description:

Searches LinkedIn, Meta Ad Library, and TikTok for ads matching a brand or keyword, then presents the results in a unified table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, researchers, and other users can compare competitors’ ad creatives and campaign activity across LinkedIn, Meta Ad Library, and TikTok. The skill returns ad details in one table for the agent to summarize.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches incur a separate charge for each page, and the external CLI’s spending-limit enforcement was not audited.

Mitigation: Review the spending plan, use a budget-limited API key, and prefer a verified, pinned CLI version.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [DataXAPI Ads on ClawHub](https://clawhub.ai/data-x-api/skills/dataxapi-ads)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [A unified table of ad details with an agent-written summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include platform, advertiser, title, copy, format, first and last shown dates, and a link. Each library page is a separately charged call.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
