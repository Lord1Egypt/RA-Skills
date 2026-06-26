## Description: <br>
CN Trends Aggregator fetches Chinese and global trend lists from Baidu, Toutiao, V2EX, Hacker News, and GitHub and formats them as JSON, text, or Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huoguang16](https://clawhub.ai/user/huoguang16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect current hot topics, technology discussions, and newly popular open-source projects for briefings, summaries, and trend discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live web requests to public trend sources, so returned items may be unavailable, incomplete, or change between runs. <br>
Mitigation: Use explicit source and limit options, and treat the output as a current snapshot rather than an authoritative record. <br>
Risk: If a proxy is configured, the proxy operator may observe request traffic. <br>
Mitigation: Use only trusted proxies and avoid proxy settings unless needed for the selected sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huoguang16/cn-trends-aggregator) <br>
- [Baidu Hot Board](https://top.baidu.com/board?tab=realtime) <br>
- [Toutiao Hot Board endpoint](https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc) <br>
- [V2EX hot topics API](https://www.v2ex.com/api/topics/hot.json) <br>
- [Hacker News top stories API](https://hacker-news.firebaseio.com/v0/topstories.json) <br>
- [GitHub repository search API](https://api.github.com/search/repositories) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON, plain text, or Markdown trend summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports source selection, item limits, output format selection, and optional HTTP proxy configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
