## Description: <br>
抖音每日最具影响力账号榜单追踪分析工具；日榜每日17:30更新/回溯7天，周榜每周一17:30更新/回溯3周，月榜每月2号9点更新/回溯3月；当用户需要查询抖音账号排名、抖音日榜/周榜/月榜、抖音赛道TOP账号或下载榜单报告时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brands, MCN teams, and analysts use this skill to query Douyin daily, weekly, and monthly account rankings, compare niche performance, and generate shareable ranking reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key. <br>
Mitigation: Provide the key only through an environment variable, confirm its scope and revocation path, and avoid exposing it in code, prompts, logs, or output files. <br>
Risk: Generated reports open in a browser and load remote JavaScript from a CDN. <br>
Mitigation: Treat generated HTML as active content and avoid opening reports in restricted or sensitive environments unless that behavior is acceptable. <br>


## Reference(s): <br>
- [API documentation](references/api_docs.md) <br>
- [Category mapping rules](references/category_map.md) <br>
- [Score calculation rules](references/score_rules.md) <br>
- [Update and date rules](references/update_rules.md) <br>
- [RedFox Douyin ranking API](https://redfox.hk/story/api/dyData/query) <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/dy-rank-tranker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown responses, JSON ranking data, shell commands, configuration snippets, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; generated HTML reports may open in a browser and load JavaScript from a CDN.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
