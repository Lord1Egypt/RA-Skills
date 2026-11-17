## Description:

Performs finance-focused web searches and local context searches using Jina, DuckDuckGo, Baidu, or a local RAG document store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve finance information from web search engines or a local daily_news database, with optional result caching, content enrichment, and sentiment scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact third-party search, content extraction, model, and LLM provider services while processing finance queries or retrieved content.

Mitigation: Review configured engines, provider credentials, and enrichment settings before use; use local search or disable enrichment and sentiment analysis when sensitive data should remain local.

Risk: Search queries, results, enriched page content, and sentiment scores may be written to the local SQLite cache.

Mitigation: Set an appropriate cache TTL, restrict access to the local database path, and avoid submitting sensitive finance queries when persistent caching is not acceptable.

Risk: Sentiment and vector search paths can load or download external model artifacts.

Mitigation: Pre-approve model sources and cached artifacts, or configure local-only models before enabling those paths.

## Reference(s):

- [AlphaEar Search Prompts](references/PROMPTS.md)
- [ClawHub alphaear-search skill page](https://clawhub.ai/zhouzhonglu8-png/skills/alphaear-search)
- [Jina Search API endpoint](https://s.jina.ai/)
- [Jina Reader API endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text summaries or structured JSON-like search result lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include titles, URLs, snippets, enriched page content, publish or crawl timestamps, source labels, and sentiment scores.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
