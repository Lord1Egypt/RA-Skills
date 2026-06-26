## Description: <br>
60s API 综合技能，提供每日新闻、AI资讯、热搜榜单、天气查询、数据查询、娱乐内容、媒体信息和实用工具。当用户询问新闻、热搜、天气、汇率、农历、笑话、运势、音乐排行、电影票房、翻译、IP查询等中文信息时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awsl1414](https://clawhub.ai/user/awsl1414) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to query Chinese-language news, trending topics, weather, exchange rates, entertainment data, media rankings, translation, IP lookup, and related utility endpoints through the 60s API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and query values to a third-party API service. <br>
Mitigation: Install only when external requests to the 60s API service are acceptable, and avoid submitting confidential text, private URLs, personal IPs, or sensitive domains. <br>
Risk: The remote password-check endpoint could expose real passwords or secrets to a third party. <br>
Mitigation: Do not use the password-check endpoint with real passwords, API keys, tokens, or other secrets. <br>


## Reference(s): <br>
- [60s API instance](https://60s.viki.moe) <br>
- [60s API documentation](https://docs.60s-api.viki.moe) <br>
- [60s API GitHub repository](https://github.com/vikiboss/60s) <br>
- [60s Skills GitHub repository](https://github.com/vikiboss/60s-skills) <br>
- [ClawHub skill page](https://clawhub.ai/awsl1414/60s-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown with inline curl commands and summarized API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded image or audio files when using media endpoints.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
