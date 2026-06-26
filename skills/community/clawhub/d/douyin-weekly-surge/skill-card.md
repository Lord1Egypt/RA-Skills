## Description: <br>
抖音七日点赞飙升榜查询工具，面向抖音作品七日新增点赞趋势查询，支持全品类或赛道筛选、默认 TOP20 展示、完整 TOP50 输出和 30 天内历史回溯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, short-video creators, MCN agencies, and data analysts use this skill to query Douyin works with rapidly increasing likes over the last seven days, filter by supported content category, review recent historical dates, and receive the result as a structured ranking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key for on-demand Douyin ranking queries. <br>
Mitigation: Provide the key only through the REDFOX_API_KEY environment variable, verify its source and scope, and avoid logging or embedding it in prompts, code, or output files. <br>
Risk: The evidence security summary flags advertised recurring subscription or push behavior as insufficiently documented. <br>
Mitigation: Use subscription features only after the publisher documents how subscriptions are created, stored, delivered, cancelled, and deleted. <br>


## Reference(s): <br>
- [API Configuration](references/api-config.md) <br>
- [Interaction Guide](references/interaction-guide.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Douyin weekly surge API endpoint](https://redfox.hk/story/api/dy/search/hotContentRank) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown ranking tables with clickable work links and short follow-up prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to TOP20 and can return up to TOP50 entries per category; requires REDFOX_API_KEY for live API access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
