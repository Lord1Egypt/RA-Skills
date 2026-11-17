## Description:

AI全链路科技资讯工厂 coordinates AI tech trend tracking, RSS collection, knowledge-card generation, and Xiaohongshu plus WeChat publishing in one workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, AI newsletter editors, and developer community operators use this skill to turn daily AI technology topics into collected source summaries, visual knowledge cards, Xiaohongshu posts, and WeChat articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can post generated content publicly.

Mitigation: Require explicit human review before publication and use restricted publishing accounts for Xiaohongshu and WeChat.

Risk: Recurring scheduled runs can repeatedly publish or save outputs without enough confirmation.

Mitigation: Use a user-scoped output directory, keep a clear disable path for cron jobs, and review scheduled runs before enabling them.

Risk: AI-generated news summaries and articles may include inaccurate or misleading claims.

Mitigation: Review source summaries and final copy against the collected RSS sources before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-tech-news-factory)
- [TechCrunch RSS feed](https://techcrunch.com/feed/)
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml)
- [MIT News artificial intelligence RSS feed](https://news.mit.edu/topic/artificial-intelligence-rss)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Image files, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports and articles, PNG knowledge cards, JSON publishing records, and optional cron command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented workflow organizes outputs under /root/articles/{date}/.]

## Skill Version(s):

1.0.0 (source: server release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
