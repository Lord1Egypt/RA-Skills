## Description: <br>
Aggregates trending topics from Weibo, Zhihu, Douyin, Baidu, 36Kr, and other public feeds, then produces AI-friendly daily hotspot reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linzmin](https://clawhub.ai/user/linzmin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI assistant users, content operators, and developers use this skill to fetch public trending-topic feeds, deduplicate entries, and generate daily Markdown and JSON reports for conversational context or content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional WeChat sending path constructs a shell command from recipient and message values. <br>
Mitigation: Avoid --send and do not schedule publishing until sending uses a non-shell argument-array API and validates recipient and message values. <br>
Risk: The scripts write reports to hard-coded OpenClaw paths. <br>
Mitigation: Review the scripts before installation and make output paths configurable and contained within the skill's own data directory before automated use. <br>
Risk: Daily reports summarize volatile public feeds and may include incomplete or unverified trending information. <br>
Mitigation: Use the generated reports as context only and verify important claims against the linked source feeds before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linzmin/ai-hotspot-daily) <br>
- [Publisher Profile](https://clawhub.ai/user/linzmin) <br>
- [RSSHub Weibo Hot Search Feed](https://rsshub.app/weibo/search/hot) <br>
- [RSSHub Zhihu Hotlist Feed](https://rsshub.app/zhihu/hotlist) <br>
- [RSSHub Douyin Hotlist Feed](https://rsshub.app/douyin/hotlist) <br>
- [RSSHub Baidu Hot Search Feed](https://rsshub.app/baidu/hotsearch) <br>
- [RSSHub 36Kr Latest News Feed](https://rsshub.app/36kr/news/latest) <br>
- [Huxiu RSS Feed](https://www.huxiu.com/rss/1.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown daily reports, structured JSON hotspot data, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public RSS and news feeds; optional WeChat sending depends on local OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
