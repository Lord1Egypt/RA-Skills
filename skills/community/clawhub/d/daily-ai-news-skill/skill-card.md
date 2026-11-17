## Description:

Aggregates and summarizes the latest AI news from multiple sources including AI news websites and web search. Provides concise news briefs with direct links to original articles. Activates when user asks for 'today's AI news', 'AI updates', 'latest AI developments', or mentions wanting a 'daily AI briefing'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laurent-zhu](https://clawhub.ai/user/laurent-zhu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to request concise daily or recent AI news briefings gathered from public AI news sources and web search. It organizes stories by announcements, research, business, tools, and policy with links, summaries, key points, and impact notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad news-related triggers may start an AI news briefing when the user intended a narrower request.

Mitigation: Invoke the skill explicitly for AI news briefings and ask for topic, source, or date-range constraints when needed.

Risk: News summaries may be incomplete, stale, or affected by source quality.

Mitigation: Verify important developments against the linked original sources and publication timestamps before relying on them.

## Reference(s):

- [Skill page](https://clawhub.ai/laurent-zhu/skills/daily-ai-news-skill)
- [AI News Sources Database](references/news_sources.md)
- [Search Query Templates](references/search_queries.md)
- [Output Format Templates](references/output_templates.md)
- [VentureBeat AI](https://venturebeat.com/category/ai/)
- [TechCrunch AI](https://techcrunch.com/category/artificial-intelligence/)
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence)
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown briefing with categorized summaries, links, key points, impact notes, and follow-up options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current public web sources; important items should be checked against linked original sources and timestamps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
