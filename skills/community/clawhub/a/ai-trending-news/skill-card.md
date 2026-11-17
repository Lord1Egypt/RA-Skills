## Description:

Fetches, ranks, and summarizes the top 10 trending AI news stories from trusted editorial, official, research, and community sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunovu20](https://clawhub.ai/user/brunovu20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to generate concise daily or weekly briefings on current AI announcements, research breakthroughs, model releases, and industry news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound requests to public news, research, and community endpoints can reveal normal connection metadata to those services.

Mitigation: Use the skill only from environments approved for outbound web access, and review or limit the configured source list when network exposure matters.

Risk: Current-news briefings can include incomplete, controversial, or weakly corroborated stories.

Mitigation: Prefer primary or reputable sources, exclude weak single-source items, and clearly label uncertainty when a story is not fully confirmed.

## Reference(s):

- [Source tiers for AI trending news](references/sources.md)
- [Ranking model](references/ranking.md)
- [ClawHub skill page](https://clawhub.ai/brunovu20/skills/ai-trending-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, JSON]

**Output Format:** [Markdown briefing with a ranked numbered list; helper script output may be JSON candidate records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exactly 10 items when at least 10 credible candidates are available; otherwise returns a smaller high-confidence set.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
