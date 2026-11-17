## Description:

AI Frontier Monitor aggregates, scores, and delivers structured AI frontier briefings from RSS feeds, 36kr, arXiv, GitHub Trending, and web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lynxpurr](https://clawhub.ai/user/lynxpurr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to collect public AI news and research signals, score candidate items, and produce concise daily or mode-specific briefings. It is intended for AI trend monitoring across product launches, technical developments, papers, repositories, and funding signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public feed titles, summaries, descriptions, and links are untrusted report data and may be misleading or adversarial.

Mitigation: Treat fetched content as data for review, not instructions, and verify important claims against original sources before relying on the briefing.

Risk: The skill can send generated output to Feishu.

Mitigation: Use explicit confirmation and a configured recipient before sending briefings outside the current conversation.

Risk: Generated briefings may overwrite the same-day archived briefing file.

Mitigation: Review the output path and keep backups or alternate filenames when preserving previous daily briefings matters.

## Reference(s):

- [Briefing Configuration](references/BRIEFING_CONFIG.md)
- [Data Sources](references/data-sources.md)
- [Scoring System](references/scoring.md)
- [ClawHub Skill Page](https://clawhub.ai/lynxpurr/skills/ai-frontier-monitor)
- [OpenAI Blog RSS](https://openai.com/blog/rss.xml)
- [Microsoft AI Blog RSS](https://blogs.microsoft.com/ai/feed)
- [AWS Machine Learning Blog RSS](https://aws.amazon.com/blogs/machine-learning/feed/)
- [arXiv API](https://export.arxiv.org/api/query)
- [GitHub Trending](https://github.com/trending?since=daily)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Shell commands, Configuration]

**Output Format:** [Chinese-language Markdown briefings with scored tiers, links, short insights, and signal summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated briefings under the skill data directory and may deliver output to a configured Feishu target.]

## Skill Version(s):

3.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
