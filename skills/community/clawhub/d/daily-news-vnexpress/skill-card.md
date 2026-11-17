## Description:

Fetch the latest trending global news from https://vnexpress.net/rss/{topic}.rss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnquyen](https://clawhub.ai/user/mrnquyen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current VNExpress RSS headlines for selected topics and summarize the returned titles, links, summaries, and publication dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to remember user behavior and write it to USERS.md, which can persist preferences or behavior beyond what is needed for news retrieval.

Mitigation: Remove the behavior logging instruction or require explicit user consent before storing any preference or behavior data.

Risk: Dependencies are listed without pinned versions.

Mitigation: Pin dependency versions before routine or production use and review updates before upgrading.

Risk: The skill fetches live RSS content and summarizes it, so freshness and source availability depend on VNExpress feeds.

Mitigation: Present publication dates and source links with summaries, and handle feed failures without treating missing results as verified news.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrnquyen/skills/daily-news-vnexpress)
- [VNExpress RSS feed template](https://vnexpress.net/rss/{topic}.rss)
- [Publisher profile](https://clawhub.ai/user/mrnquyen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with RSS-derived news titles, links, summaries, and publication dates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live RSS data for predefined VNExpress topics and a requested item count.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
