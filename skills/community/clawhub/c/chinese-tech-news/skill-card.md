## Description: <br>
采集钛媒体、虎嗅、36氪、爱范儿四大中文科技媒体的最新资讯，整理成带原文链接的快讯。无需 API Key，直接抓取 RSS 源。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ofaith](https://clawhub.ai/user/ofaith) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch a concise snapshot of recent Chinese technology news from public RSS feeds and review source links for each headline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill sends network requests to the configured public media RSS feeds. <br>
Mitigation: Use it only in environments where outbound requests to those news sites are acceptable. <br>
Risk: The skill prints links from external news sources. <br>
Mitigation: Review printed links before opening them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ofaith/chinese-tech-news) <br>
- [TMTPost RSS feed](https://www.tmtpost.com/rss) <br>
- [Huxiu RSS feed](https://www.huxiu.com/rss/0.xml) <br>
- [36Kr RSS feed](https://36kr.com/feed) <br>
- [ifanr RSS feed](https://www.ifanr.com/feed) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output with numbered headlines, source names, and original links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public RSS feeds at runtime and prints approximately 20 headline links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
