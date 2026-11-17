## Description:

Aggregates and summarizes the latest AI news from multiple sources including AI news websites and web search, using Tavily API when available or Brave Search as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather recent AI news, filter duplicate or stale items, organize stories by category, and produce concise daily briefings with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends AI-news queries and article URLs to external search or web-reading services.

Mitigation: Use only in environments where outbound browsing and the configured search provider are acceptable.

Risk: The preferred Tavily workflow uses an API key.

Mitigation: Provide TAVILY_API_KEY only through approved secret management and avoid exposing it in prompts, logs, or shared outputs.

Risk: Current-news summaries can be incomplete, duplicated, stale, or based on inaccessible article excerpts.

Mitigation: Prefer full article retrieval when available, keep source links in the briefing, and review high-impact claims before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/litiao1224/skills/daily-ai-news-skill-litiao)
- [AI News Sources Database](artifact/references/news_sources.md)
- [Search Query Templates](artifact/references/search_queries.md)
- [Output Format Templates](artifact/references/output_templates.md)
- [VentureBeat AI](https://venturebeat.com/category/ai/)
- [TechCrunch AI](https://techcrunch.com/category/artificial-intelligence/)
- [MIT Technology Review AI](https://www.technologyreview.com/topic/artificial-intelligence/)
- [OpenAI Blog](https://openai.com/blog)
- [Anthropic News](https://www.anthropic.com/news)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown briefings with categorized summaries, key points, source dates, and links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce brief, standard, or deep AI news formats over configurable time ranges and focus areas.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
