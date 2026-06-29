## Description: <br>
抖音作品爬取工具，输入抖音名称或抖音ID，输出抖音账号基础信息和近期作品内容列表（最多50条）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brands, MCN operators, content creators, and data analysts use this skill to retrieve recent Douyin account works and engagement summaries from RedFox APIs for monitoring, evaluation, content analysis, and report preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Douyin names or IDs to RedFox APIs and consumes a RedFox API key or credits. <br>
Mitigation: Install and use it only when RedFox data submission and API-key use are acceptable for the account being queried. <br>
Risk: The command-line script prints the first characters of the configured API key. <br>
Mitigation: Avoid running it in shared logs, screenshots, or recorded sessions until the partial API-key print is removed. <br>
Risk: Nickname searches can return a fuzzy or unintended Douyin account. <br>
Mitigation: Use precise Douyin IDs when querying accounts or submitting accounts for indexing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/redfox-data/douyin-works-crawler) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?souce=github) <br>
- [RedFox data platform](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, guidance] <br>
**Output Format:** [Markdown report or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recent works are capped at 50 items; results may include account indexing guidance when no account is found.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version, released 2026-06-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
