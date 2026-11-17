## Description:

Queries Douyin daily like-surge rankings, returning top works by new likes with category filtering and up to 30 days of historical lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content operators, short-video creators, MCN agencies, and data analysts use this skill to monitor Douyin works with fast single-day like growth, compare categories, and review recent ranking history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends Douyin ranking queries to redfox.hk.

Mitigation: Use a scoped and revocable RedFox key when available, provide it through the environment instead of hardcoding it, and install only if sharing those queries with RedFox is acceptable.

Risk: The skill advertises scheduled subscription pushes without clear evidence for storage, opt-out, or retention controls.

Mitigation: Enable subscription behavior only after the publisher documents scheduling, stored preferences, opt-out controls, and retention.

Risk: Returned video links are rendered as clickable Markdown links and are not strongly validated by the script.

Mitigation: Review links before opening them and treat unexpected Douyin or third-party URLs cautiously.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/douyin-content-surge-redfox)
- [API configuration](references/api-config.md)
- [Interaction guide](references/interaction-guide.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox Douyin ranking API endpoint](https://redfox.hk/story/api/dy/search/hotContentRank)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown ranking tables with clickable work links, plus concise text guidance and configuration snippets when setup is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to top 20 ranking rows and can return up to 50 rows per category; historical queries are limited to the past 30 days.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
