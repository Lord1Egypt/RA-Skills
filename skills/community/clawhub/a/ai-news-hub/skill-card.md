## Description:

AI News Hub helps agents aggregate AI and technology news from RSS feeds, arXiv papers, GitHub Trending, and company updates into news briefings, reports, and filtered summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingcodingking](https://clawhub.ai/user/kingcodingking)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor AI and technology news, recent research papers, GitHub project trends, and company updates. Agents can use it to produce daily or weekly briefings, keyword-specific summaries, and category-filtered news views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL summarizer can fetch arbitrary user-provided URLs and may forward those URLs to a third-party parser.

Mitigation: Do not provide private, signed, localhost, internal-network, or file URLs; run the skill in a network-restricted environment when possible.

Risk: The skill contacts many external RSS, arXiv, and GitHub sources during normal use.

Mitigation: Review artifact/scripts/rss_sources.json before deployment and limit categories, date ranges, or network access to match the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingcodingking/skills/ai-news-hub)
- [Artifact homepage link](https://github.com/lanyasheng/ai-news-aggregator)
- [arXiv API endpoint used by helper script](http://export.arxiv.org/api/query?)
- [RSS source configuration](artifact/scripts/rss_sources.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Chinese-language Markdown or plain text summaries, with optional JSON output from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include article titles, source names, URLs, timestamps, relevance scores, categories, and daily or weekly report sections.]

## Skill Version(s):

2.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
