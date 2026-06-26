## Description: <br>
抖音每日最热作品榜查询工具，可查询单日点赞 TOP50 榜单，支持按赛道分类、最多 30 天历史回溯和订阅推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as content operators, creators, brands, MCNs, and analysts use this skill to retrieve Douyin daily hot-work rankings, compare category performance, and review recent content trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a REDFOX_API_KEY and sends it to redfox.hk for ranking queries. <br>
Mitigation: Configure the key through the host environment, do not hard-code it in prompts or files, and use only keys that can be reset or revoked. <br>
Risk: Subscription or recurring push behavior could send ranking updates beyond a one-time query. <br>
Mitigation: Enable subscriptions only after clear user confirmation and provide a visible way to disable them. <br>
Risk: Ranking data reflects stored snapshot timing rather than live Douyin metrics. <br>
Mitigation: Tell users that interaction counts are snapshot data and may differ from real-time platform values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/douyin-daily-hot) <br>
- [API configuration](references/api-config.md) <br>
- [Interaction guide](references/interaction-guide.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox service](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown ranking tables with clickable work links, brief status messages, and API key setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to TOP20 results and can show the full TOP50 when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
