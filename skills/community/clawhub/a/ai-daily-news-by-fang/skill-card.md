## Description:

Tracks recent AI technical developments across models, tools, research ideas, and community projects, then produces a Chinese markdown daily news summary with original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangziyang0910](https://clawhub.ai/user/fangziyang0910)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent AI technology news and generate a ranked Chinese daily report. It focuses on models, tools, research ideas, and community projects while excluding business, funding, and policy news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be sent to a configured Feishu recipient without a clear per-run confirmation step.

Mitigation: Verify the recipient open_id before installation and require manual confirmation before sending when reports may contain sensitive or unreviewed information.

Risk: The skill fetches and summarizes current web content, so generated reports may include stale, incomplete, or inaccurate source material.

Mitigation: Review cited original links and timestamps before relying on or forwarding the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangziyang0910/skills/ai-daily-news-by-fang)
- [AI news source list](references/sources.md)
- [QbitAI](https://www.qbitai.com)
- [Jiqizhixin](https://www.jiqizhixin.com)
- [Hacker News](https://news.ycombinator.com/)
- [OpenAI Blog](https://openai.com/index)
- [Anthropic News](https://www.anthropic.com/news)
- [Claude Code changelog](https://code.claude.com/docs/en/changelog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown daily report with original links, saved as a dated local file and sent as a Feishu message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks items by heat and filters to AI technical developments from the last 3 days.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
