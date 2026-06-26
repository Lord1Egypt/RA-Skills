## Description: <br>
定时访问指定电商或社交平台页面，抓取点赞、评论、销量等数据，检测异常波动，自动截图并发送提醒通知。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hwl1413520](https://clawhub.ai/user/hwl1413520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
市场、运营和数据分析人员使用该技能定时监控竞品页面的关键指标，发现异常增长或潜在爆款并接收告警。开发者也可用它配置抓取任务、阈值、截图和通知渠道。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured scraping jobs may target sites where automated access is restricted or inappropriate. <br>
Mitigation: Review each monitored URL before use, confirm that collection is allowed, and use conservative schedules and retention settings. <br>
Risk: Alert screenshots and archived monitoring data can capture private account, customer, or business information. <br>
Mitigation: Disable screenshot_on_alert for sensitive pages, restrict access to screenshot and data directories, and apply the configured retention periods. <br>
Risk: Webhook and email notification settings can expose credentials or route alerts to unintended recipients. <br>
Mitigation: Store webhook tokens and email credentials as protected secrets, review notification destinations, and avoid committing live credentials in task configuration. <br>
Risk: The installer and browser automation dependencies execute local setup and network-facing automation. <br>
Mitigation: Review the installer before running it and install the skill inside a virtual environment or container. <br>


## Reference(s): <br>
- [Platform CSS Selector Reference](artifact/references/PLATFORM_SELECTORS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hwl1413520/competitor-monitor-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include monitored URLs, schedules, metric selectors, alert thresholds, screenshot settings, and notification channel configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
