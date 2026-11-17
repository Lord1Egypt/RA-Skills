## Description:

Aggregate and deduplicate AI news from multiple Chinese and English tech news sources into a single merged digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch current AI news from multiple Chinese and English technology sources, merge duplicate stories, categorize the results, and produce a concise digest in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on web access to public news pages and search results, so some sources may be unavailable or return incomplete results.

Mitigation: Continue with available sources, disclose failed sources in the digest, and use broad web search only as a last resort.

Risk: Current news aggregation can include duplicate, stale, or incorrectly summarized stories.

Mitigation: Deduplicate by comparing titles and topics, include source links for review, and keep briefs concise.

## Reference(s):

- [TechNews AI](https://technews.tw/category/ai/)
- [QbitAI](https://www.qbitai.com/)
- [TechNice AI](https://www.technice.com.tw/category/issues/ai/)
- [AIBase Daily](https://news.aibase.com/zh/daily)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown news digest with categorized numbered lists, brief summaries, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output language follows the user's query language; mixed-language requests default to Chinese.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
