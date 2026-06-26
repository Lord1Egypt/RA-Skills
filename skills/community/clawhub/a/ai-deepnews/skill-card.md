## Description: <br>
AI Product Manager daily intelligence digest that fetches news from 16+ curated RSS sources, translates results to Chinese, deduplicates articles, filters by date, and requires no API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Janettbella69](https://clawhub.ai/user/Janettbella69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI product managers, technical teams, and individual practitioners use this skill to collect recent AI news from media, lab blogs, research feeds, developer communities, and podcasts, then produce a Chinese Markdown digest for daily or weekly intelligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts multiple public RSS sources and Google Translate, so fetched article content and summaries leave the local environment during normal use. <br>
Mitigation: Run it only in environments where outbound requests to the listed sources and translation service are acceptable. <br>
Risk: Generated article text and links may contain misleading, stale, or untrusted news content. <br>
Mitigation: Review digest entries and source links before using them in agent workflows, reports, or automated downstream actions. <br>
Risk: The skill writes a local Markdown digest and seen-article cache. <br>
Mitigation: Review local file retention expectations and clear latest_digest.md or seen_articles.json when cached news history should not persist. <br>


## Reference(s): <br>
- [AI DeepNews ClawHub listing](https://clawhub.ai/Janettbella69/ai-deepnews) <br>
- [TechCrunch AI RSS](https://techcrunch.com/category/artificial-intelligence/feed/) <br>
- [OpenAI Blog RSS](https://openai.com/blog/rss.xml) <br>
- [Google AI Blog RSS](https://blog.google/technology/ai/rss/) <br>
- [arXiv cs.AI RSS](https://rss.arxiv.org/rss/cs.AI) <br>
- [Hugging Face Blog RSS](https://huggingface.co/blog/feed.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown digest printed to stdout and written to latest_digest.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches up to 30 recent articles, limits each feed to 5 articles, filters articles older than 3 days, and stores a local seen_articles.json cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
