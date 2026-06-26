## Description: <br>
抖音每日点赞飙升榜 returns daily Douyin works ranked by new likes, with category filters, clickable video links, and up to 30 days of historical lookback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, short-video creators, MCN agencies, and data analysts use this skill to query Douyin daily like-surge rankings, filter results by content category, and review recent historical trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires REDFOX_API_KEY and sends that key to redfox.hk when ranking queries run. <br>
Mitigation: Install only after verifying trust in RedFoxHub, keep the key in environment or agent configuration, and avoid placing keys in prompts, logs, code, or output files. <br>
Risk: Broad surge-ranking requests may activate the skill unexpectedly. <br>
Mitigation: Use explicit Douyin ranking wording when invoking the skill and review the selected category and date before relying on results. <br>
Risk: Ranking data is constrained to yesterday-or-earlier updates and a 30-day lookback window. <br>
Mitigation: Tell users when a requested date is unavailable and return the closest supported date range rather than presenting unavailable data as current. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/douyin-content-surge-redfox) <br>
- [API configuration](references/api-config.md) <br>
- [Interaction guide](references/interaction-guide.md) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox Douyin ranking endpoint](https://redfox.hk/story/api/dy/search/hotContentRank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown table with clickable Douyin video links, brief status text, and optional subscription guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to TOP20 results; supports full TOP50 output, category filtering, and 30-day historical date queries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
