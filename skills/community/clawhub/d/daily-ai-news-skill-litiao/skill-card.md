## Description: <br>
Aggregates and summarizes the latest AI news from multiple sources including AI news websites and web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather recent AI news, filter and categorize stories, and produce a concise briefing with links to original sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search API use can consume Tavily quota or fail when TAVILY_API_KEY is missing or invalid. <br>
Mitigation: Use a key with acceptable quota limits and rely on the documented web-search fallback when Tavily is unavailable. <br>
Risk: Current-news summaries may include outdated, duplicated, or inaccurate claims from fetched articles or search snippets. <br>
Mitigation: Review the linked original sources for important stories before acting on the briefing. <br>
Risk: The workflow references an external Tavily helper skill that is not included in this artifact. <br>
Mitigation: Verify that helper before relying on Tavily-based collection, or use direct website fetching and web-search fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/daily-ai-news-skill-litiao) <br>
- [AI News Sources Database](references/news_sources.md) <br>
- [Output Format Templates](references/output_templates.md) <br>
- [Search Query Templates](references/search_queries.md) <br>
- [VentureBeat AI](https://venturebeat.com/category/ai/) <br>
- [TechCrunch AI](https://techcrunch.com/category/artificial-intelligence/) <br>
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence) <br>
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefing with categorized summaries, source links, and optional shell commands for search helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require TAVILY_API_KEY for preferred search workflow; falls back to web search when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
