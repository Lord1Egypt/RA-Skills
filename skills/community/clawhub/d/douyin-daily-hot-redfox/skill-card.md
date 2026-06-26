## Description: <br>
抖音每日热门作品榜 queries RedFox for Douyin daily likes rankings and returns category-filtered, date-scoped ranking results as Markdown tables with links to the original works. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operations teams, creators, brands, MCNs, and analysts use this skill to check Douyin daily hot works, compare category rankings, and review recent historical trends. It is useful when an agent needs concise TOP20 or TOP50 ranking output from RedFox data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided RedFox API key and sends Douyin ranking queries to redfox.hk. <br>
Mitigation: Use a scoped, revocable API key, store it only in the REDFOX_API_KEY environment variable, and avoid exposing it in prompts, logs, code, or output files. <br>
Risk: Ranking results depend on RedFox data availability and may differ from live Douyin engagement metrics. <br>
Mitigation: Treat results as snapshot ranking data, confirm the requested date and category, and avoid relying on broad triggers such as "show all" without context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/douyin-daily-hot-redfox) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [API configuration](references/api-config.md) <br>
- [Interaction guide](references/interaction-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables with linked Douyin work titles, short explanatory text, and optional shell configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to TOP20 results, can return up to TOP50, supports category filters and up to 30 days of historical lookback.] <br>

## Skill Version(s): <br>
1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
