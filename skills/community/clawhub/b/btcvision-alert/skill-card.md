## Description: <br>
Send automatic Bitcoin price alerts when BTC moves +/-3% or crosses key levels, using BTCvision.org live data and notifications for Telegram, Discord, and Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welove111](https://clawhub.ai/user/welove111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto-monitoring users use this skill to check Bitcoin price and sentiment data, then trigger recurring alerts when BTC moves sharply, crosses a target level, or sentiment reaches extreme values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alerts rely on BTCvision.org for live Bitcoin price and sentiment data. <br>
Mitigation: Confirm that BTCvision.org is an acceptable data source before relying on the alerts. <br>
Risk: The alert template may post donation text or other content into shared messaging channels. <br>
Mitigation: Review and edit the alert template before connecting Telegram, Discord, or Slack. <br>
Risk: Recurring cron checks and messaging integrations can create repeated notifications. <br>
Mitigation: Enable scheduled checks only when recurring alerts are intended and the notification channel is appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/welove111/btcvision-alert) <br>
- [BTCvision homepage](https://btcvision.org) <br>
- [BTCvision MCP endpoint](https://btcvision.org/.netlify/functions/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with API examples, alert template text, JavaScript condition snippets, and cron command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live BTCvision.org data and optional recurring checks through cron or messaging integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
