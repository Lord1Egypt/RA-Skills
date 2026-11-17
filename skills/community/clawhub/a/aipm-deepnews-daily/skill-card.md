## Description:

AI Product Manager daily intelligence digest. Fetches news from 16+ curated RSS sources across tech media, AI labs, research papers, developer communities, and podcasts. Auto-translates to Chinese with deduplication and date filtering. Zero API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janettbella69](https://clawhub.ai/user/janettbella69)

### License/Terms of Use:

MIT-0

## Use Case:

AI product managers, technical teams, and individual AI practitioners use this skill to collect recent AI news, translate titles and summaries into Chinese, deduplicate items, and produce a Markdown digest for daily or weekly intelligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs automatic network access to public RSS feeds and sends article titles and summaries to Google Translate.

Mitigation: Use it only where that data sharing is acceptable, and review or restrict the configured feeds before operational use.

Risk: Generated Markdown contains external news content and links that may be inaccurate, stale, or unsafe to follow.

Mitigation: Treat the digest as untrusted content, verify important claims against original sources, and review links before following them or passing the digest to another agent.

Risk: Runtime dependencies are installed from package indexes and include an unreleased candidate translation package.

Mitigation: Pin and review dependencies before repeated or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/janettbella69/skills/aipm-deepnews-daily)
- [Publisher profile](https://clawhub.ai/user/janettbella69)
- [TechCrunch AI RSS feed](https://techcrunch.com/category/artificial-intelligence/feed/)
- [OpenAI Blog RSS feed](https://openai.com/blog/rss.xml)
- [Google AI RSS feed](https://blog.google/technology/ai/rss/)
- [DeepMind Blog RSS feed](https://deepmind.google/blog/rss.xml)
- [Anthropic RSS feed](https://www.anthropic.com/rss.xml)
- [Hugging Face Blog RSS feed](https://huggingface.co/blog/feed.xml)
- [arXiv cs.AI RSS feed](https://rss.arxiv.org/rss/cs.AI)
- [arXiv cs.CL RSS feed](https://rss.arxiv.org/rss/cs.CL)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown digest written to stdout and latest_digest.md, with setup and usage commands in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 5 articles per feed and 30 total articles, filters to recent items, caches seen article identifiers for seven days, and falls back to original text when translation fails.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
