## Description: <br>
飞书每日早报配置Skill。封装了每日早报的完整配置流程，包含数据源获取、格式整理、深圳天气查询、生活建议整合。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[easyhoov](https://clawhub.ai/user/easyhoov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or teams use this skill to generate a daily Feishu morning briefing with news, configurable city weather, short work/life/health suggestions, and a daily quote. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled push scripts can send the generated morning briefing to a fixed Feishu recipient. <br>
Mitigation: Review or disable the push scripts before installation, and replace the recipient with a validated user-controlled configuration before enabling delivery. <br>
Risk: Automated Feishu delivery may occur without a clear preview or confirmation step. <br>
Mitigation: Require a preview or confirmation workflow before sending and grant Feishu messaging permissions only when the documented behavior matches the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/easyhoov/feishu-morning-news) <br>
- [60s news API](https://60s.viki.moe/v2/60s) <br>
- [Configuration reference](references/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown daily briefing content; bundled scripts can send text content to Feishu.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configurable city, news data source, push time, retry count, and Feishu recipient configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
