## Description:

Collects, filters, categorizes, and summarizes game-industry AI news from public RSS feeds and API-backed news sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuhuimin0224-create](https://clawhub.ai/user/zhuhuimin0224-create)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and game-industry teams use this skill to retrieve Chinese and English game-AI daily or weekly briefings, filtered by categories such as AI content creation, in-game AI, development tools, operations, industry news, and research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live searches may send confidential project names or private strategy terms to third-party services.

Mitigation: Use only public or non-sensitive search terms when requesting live game-AI news.

Risk: Generated news briefs may contain outdated, incomplete, or secondary-source summaries.

Mitigation: Verify source links and original publications before relying on a report for important business or technical decisions.

Risk: The skill writes local daily cache files during normal operation.

Mitigation: Deploy it only in workspaces where local cache-file creation under the skill data directory is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuhuimin0224-create/skills/ai-game)
- [Source catalog](references/sources.json)
- [Keyword and category filters](references/keywords.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news brief with titles, links, summaries, details, recommendations, and optional JSON-backed source data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily reports are normally limited to 10 items and weekly reports to 15 items; generated cache files are written under data/YYYY-MM-DD.json.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
