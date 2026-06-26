## Description: <br>
每日推送中国热榜TOP10到飞书。从微博、知乎、百度、36氪筛选最重要的新闻，智能排除明星八卦和主观评论。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgolye](https://clawhub.ai/user/imgolye) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to receive a concise daily TOP10 summary of major Chinese trending topics from Weibo, Zhihu, Baidu, and 36Kr, with entertainment gossip, advertisements, and subjective commentary filtered out. It can be triggered manually or scheduled through OpenClaw Cron for delivery to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled Feishu delivery can send recurring messages to the wrong recipient or at an unwanted time if the cron example is configured incorrectly. <br>
Mitigation: Confirm the Feishu recipient, timezone, and schedule before enabling the cron job, and keep the removal command or process available. <br>
Risk: Trending-topic summaries may include incomplete or misleading public hot-list information. <br>
Mitigation: Review important items before acting on them and treat the generated list as a news-summary aid rather than an authoritative source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imgolye/daily-hot-push) <br>
- [Weibo hot search source](https://tophub.today/n/KqndgxeLl9) <br>
- [Zhihu hot list source](https://tophub.today/n/mproPpoq6O) <br>
- [Baidu real-time hot topics source](https://tophub.today/n/Jb0vmloB1G) <br>
- [36Kr 24-hour hot list source](https://tophub.today/n/Q1Vd5Ko85R) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with numbered news items and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a concise 10-item news summary intended for manual reading or scheduled Feishu delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
