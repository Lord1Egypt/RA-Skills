## Description:

每日简报生成器自动收集新闻、热点和行业动态，并生成结构化中文简报，适合每天早上获取当日信息摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwfqls3w-cmd](https://clawhub.ai/user/wwfqls3w-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to gather current news, technology, business, finance, and industry items into a concise Chinese Markdown briefing for personal review or team sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched article text and links may contain inaccurate, misleading, or untrusted public web content.

Mitigation: Review generated briefings as untrusted news data and verify important stories against the original source before relying on them.

Risk: Remote article fields are not escaped or URL-validated before appearing in the generated briefing.

Mitigation: Use caution when opening links from generated briefings and inspect unfamiliar URLs before clicking.

Risk: Network source availability can affect briefing completeness and quality.

Mitigation: Run the skill in an environment with access to the configured public sources and treat missing or sparse sections as incomplete coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwfqls3w-cmd/skills/cn-daily-briefing)
- [ClawHub homepage metadata](https://clawhub.ai/skills/cn-daily-briefing)
- [Hacker News API top stories](https://hacker-news.firebaseio.com/v0/topstories.json)
- [36Kr RSS feed](https://36kr.com/feed)
- [V2EX hot feed](https://www.v2ex.com/feed/tab/hot.xml)
- [InfoQ China feed](https://www.infoq.cn/feed)
- [GitHub Trending](https://github.com/trending?since=daily)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown briefing with source links and optional local Markdown file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch public web content and save generated briefings under the user's daily-briefings directory or a user-specified output path.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
