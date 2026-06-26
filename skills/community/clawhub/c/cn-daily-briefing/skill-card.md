## Description: <br>
每日简报生成器自动收集新闻、热点和行业动态，生成结构化中文简报，适合每天早上获取当日信息摘要。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwfqls3w-cmd](https://clawhub.ai/user/wwfqls3w-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users and teams use this skill to collect current public news and developer information, classify it by topic, and produce a concise Markdown briefing for daily reading or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public news and developer sites when a briefing is requested. <br>
Mitigation: Run it only in environments where those public network requests are acceptable. <br>
Risk: Generated briefings can contain incomplete, stale, or misleading summaries from upstream sources. <br>
Mitigation: Verify important items against original sources before using them for decisions. <br>
Risk: The fetch script can save generated Markdown reports locally. <br>
Mitigation: Review the output path and stored reports if local persistence is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwfqls3w-cmd/cn-daily-briefing) <br>
- [Skill homepage](https://clawhub.ai/skills/cn-daily-briefing) <br>
- [Hacker News top stories API](https://hacker-news.firebaseio.com/v0/topstories.json) <br>
- [36Kr RSS feed](https://36kr.com/feed) <br>
- [V2EX hot feed](https://www.v2ex.com/feed/tab/hot.xml) <br>
- [InfoQ Chinese feed](https://www.infoq.cn/feed) <br>
- [GitHub Trending daily](https://github.com/trending?since=daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with categorized headlines, summaries, source links, and optional shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated Markdown reports locally when the bundled fetch script is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
