## Description:

Aggregates and summarizes the latest AI news from multiple sources including AI news websites and web search, then provides concise news briefs with direct links to original articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khurramjamil12](https://clawhub.ai/user/khurramjamil12)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request daily AI news briefings, recent AI developments, or focused updates on AI research, industry, tools, policy, and ethics. The skill gathers current web sources, filters and deduplicates stories, and returns a categorized briefing with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may contact third-party news sites and search providers.

Mitigation: Use the skill only in environments where external browsing is permitted, and avoid including private or sensitive context in news requests.

Risk: News briefings can become stale or inaccurate if source pages change, links fail, or duplicate coverage is not filtered.

Mitigation: Verify publication dates, source links, and source diversity before relying on a briefing for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khurramjamil12/skills/daily-ai-news-skill-0-1-0)
- [AI News Sources Database](references/news_sources.md)
- [Search Query Templates](references/search_queries.md)
- [Output Format Templates](references/output_templates.md)
- [VentureBeat AI](https://venturebeat.com/category/ai/)
- [TechCrunch AI](https://techcrunch.com/category/artificial-intelligence/)
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence)
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown news briefing with categorized summaries, key points, impact notes, timestamps, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports brief, standard, deep, chronological, company-focused, category-focused, and custom time-range briefing formats.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
