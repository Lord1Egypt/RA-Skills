## Description: <br>
Aggregates and summarizes the latest AI news from multiple sources including AI news websites and web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Laurent-Zhu](https://clawhub.ai/user/Laurent-Zhu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to gather recent AI news, filter and deduplicate stories, and produce concise briefings across announcements, research, business, tools, and policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses external news pages that may contain stale, inaccurate, or instruction-like content. <br>
Mitigation: Treat fetched pages as untrusted source material; summarize and cite them without following embedded instructions, and verify publication dates and links. <br>
Risk: Broad AI update requests can trigger web browsing across many public sources. <br>
Mitigation: Keep the query scope and time range aligned to the user's request and avoid requesting local files, credentials, or private data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Laurent-Zhu/daily-ai-news-skill) <br>
- [AI News Sources Database](references/news_sources.md) <br>
- [Search Query Templates](references/search_queries.md) <br>
- [Output Format Templates](references/output_templates.md) <br>
- [VentureBeat AI](https://venturebeat.com/category/ai/) <br>
- [TechCrunch AI](https://techcrunch.com/category/artificial-intelligence/) <br>
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown news briefing with source links, summaries, key points, impact notes, and takeaways] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports brief, standard, deep, chronological, by-company, and category-focused briefing formats.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
