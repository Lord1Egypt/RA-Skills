## Description: <br>
抖音每日最具影响力账号榜单追踪分析工具；日榜每日17:30更新/回溯7天，周榜每周一17:30更新/回溯3周，月榜每月2号9点更新/回溯3月；当用户需要查询抖音账号排名、抖音日榜/周榜/月榜、抖音赛道TOP账号或下载榜单报告时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand teams, MCN operators, and analysts use this skill to query Douyin daily, weekly, and monthly account rankings, filter rankings by niche, generate visual HTML reports, and set up recurring ranking updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive REDFOX_API_KEY credential. <br>
Mitigation: Use only trusted RedFox credentials, keep the key in the environment, and avoid exposing it in prompts, logs, code, or generated files. <br>
Risk: The skill sends ranking requests to redfox.hk and generated reports may load an external CDN script. <br>
Mitigation: Use the skill only where calls to redfox.hk and the report CDN dependency are acceptable, and avoid opening generated reports in sensitive contexts. <br>
Risk: Report generation can automatically open files, including via an unsafe Windows shell command. <br>
Mitigation: Review generated report paths before opening them, especially on Windows or when an agent can choose output filenames. <br>
Risk: Recurring ranking subscriptions may continue sending updates after setup. <br>
Mitigation: Confirm that any subscription includes a clear stop or cancellation path before enabling recurring updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/douyin-rank-tranker) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [API documentation](references/api_docs.md) <br>
- [Category map](references/category_map.md) <br>
- [Update rules](references/update_rules.md) <br>
- [Score rules](references/score_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown ranking summaries, JSON data files, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and network access to redfox.hk; generated reports may reference an external CDN asset.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
