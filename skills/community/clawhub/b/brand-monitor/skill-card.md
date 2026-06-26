## Description: <br>
新能源汽车品牌舆情监控 - 自动搜索、分析国内平台的品牌提及情况 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenxiaoyu](https://clawhub.ai/user/wenxiaoyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External brand, communications, and customer-experience teams use this skill to monitor new-energy vehicle brand mentions across Chinese platforms, analyze sentiment and influence, detect urgent issues, and produce monitoring, alert, and trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses shell execution to run a crawler. <br>
Mitigation: Review the skill before installing, restrict who can invoke it, and use only trusted brand names and configuration values. <br>
Risk: SerpAPI keys and Feishu webhook URLs are secrets that may be exposed through configuration or logs. <br>
Mitigation: Store SERPAPI_KEY and Feishu webhook URLs as secrets, avoid committing real values, and rotate them if exposure is suspected. <br>
Risk: Feishu or SMS alerting can send monitored data to third-party reporting destinations. <br>
Mitigation: Do not enable Feishu or SMS alerts until the data being sent, recipients, and operational controls are understood. <br>
Risk: Scheduled runs and memory retention can repeatedly collect and retain brand-monitoring data. <br>
Mitigation: Avoid enabling scheduled runs or memory retention until retention, access, and review expectations are defined. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenxiaoyu/brand-monitor) <br>
- [README.md](README.md) <br>
- [如何使用Skill.md](如何使用Skill.md) <br>
- [使用指南-SerpAPI版.md](使用指南-SerpAPI版.md) <br>
- [SerpAPI usage guide](crawler/SerpAPI使用指南.md) <br>
- [获取飞书Webhook指南.md](获取飞书Webhook指南.md) <br>
- [SerpAPI](https://serpapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured sections, JSON crawler results, inline shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include sentiment scores, influence estimates, platform breakdowns, alert severity, recommended actions, and Feishu webhook delivery instructions.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, release metadata, changelog released 2026-02-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
