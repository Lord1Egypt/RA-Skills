## Description:

Scrape Reddit posts, comments, subreddits, and users with the Apify Reddit Scraper Actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshmaur](https://clawhub.ai/user/harshmaur)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public Reddit posts, comments, user histories, and community information for monitoring, research, and lead discovery. It can return structured results and optionally send them to user-selected services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify runs can incur variable charges, especially when collecting comments or searching multiple terms.

Mitigation: Review expected costs and set an explicit spending limit before running the skill.

Risk: Results are stored in the cloud and may be forwarded to selected destinations or recurring workflows.

Mitigation: Choose trusted destinations and schedules deliberately, and review data handling before enabling delivery.

## Reference(s):

- [ClawHub release](https://clawhub.ai/harshmaur/skills/apify-reddit-scraper)
- [Apify MCP integration documentation](https://docs.apify.com/platform/integrations/mcp)
- [Input mapping reference](references/input-mapping.md)
- [Known gotchas](references/gotchas.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [Structured Reddit records with concise summaries or reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include posts, comments, user profiles, and community information; optional delivery uses user-selected connectors.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
