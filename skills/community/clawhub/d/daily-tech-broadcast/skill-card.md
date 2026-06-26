## Description: <br>
从可抓取信息源（新浪科技、IT之家等）拉取当日科技新闻标题，生成简报并输出。无需 API Key，适合定时任务与手动触发。当用户要求执行每日科技播报、科技新闻简报、今日科技要闻时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyaok1](https://clawhub.ai/user/wangyaok1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to generate a daily technology news digest from configurable public news sources for manual requests or scheduled channel delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to third-party news sources. <br>
Mitigation: Install only where outbound requests to those sources are acceptable, especially for scheduled execution. <br>
Risk: Scheduled delivery can publish third-party news summaries into shared or public channels without review. <br>
Mitigation: Configure cron delivery only for appropriate channels and consider reviewing output before posting in shared or public spaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangyaok1/daily-tech-broadcast) <br>
- [Sina Tech](https://tech.sina.com.cn/) <br>
- [IT Home](https://www.ithome.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted plain text digest printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches up to 12 headlines from configured sources and emits fallback text when fetching fails.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
