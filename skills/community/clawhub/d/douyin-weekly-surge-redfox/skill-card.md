## Description: <br>
抖音七日点赞飙升榜查询工具，使用 RedFox API 输出全平台抖音作品七日新增点赞 TOP50 榜单，并支持赛道分类查询和最多 30 天历史回溯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, short-video creators, MCN agencies, and data analysts use this skill to monitor Douyin works with strong seven-day like growth, compare category trends, review recent history, and receive opt-in ranking updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key. <br>
Mitigation: Create and store the key only if you trust the RedFox service, keep it in REDFOX_API_KEY or the agent environment, and avoid hardcoding or exposing it in prompts, logs, or output files. <br>
Risk: Subscription or push-delivery behavior could create ongoing notifications or data access after a one-time query. <br>
Mitigation: Enable subscriptions only after explicit user opt-in, and confirm storage, schedule, and cancellation behavior before activation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuanyi-github/douyin-weekly-surge-redfox) <br>
- [API Configuration](references/api-config.md) <br>
- [Interaction Guide](references/interaction-guide.md) <br>
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown ranking tables with clickable Douyin work links and concise natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to TOP20 results; can output up to TOP50 per category; requires REDFOX_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
