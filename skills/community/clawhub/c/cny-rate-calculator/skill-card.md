## Description: <br>
Fetches Bank of Taiwan CNY exchange rates, calculates tiered pricing with configured discounts, and sends scheduled notifications through selected messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[9Starmax](https://clawhub.ai/user/9Starmax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to monitor Bank of Taiwan CNY exchange rates, calculate tiered prices, and deliver alerts through configured OpenClaw messaging channels on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read OpenClaw messaging configuration, use channel credentials, and send exchange-rate notifications to selected destinations. <br>
Mitigation: Review configured channels, webhook URLs, TELEGRAM_BOT_TOKEN, OPENCLAW_GATEWAY_TOKEN, and OPENCLAW_GATEWAY_URL before enabling notifications. <br>
Risk: The skill can create or update a recurring OpenClaw cron job for scheduled execution. <br>
Mitigation: Confirm the cron expression, destination channels, and expected schedule before enabling auto-setup or scheduled notifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/9Starmax/cny-rate-calculator) <br>
- [Bank of Taiwan exchange rates](https://rate.bot.com.tw/xrt) <br>
- [Prairie Grasslands calculator reference](https://78lion.com/CNY.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown-style messages, terminal output, JSON channel status, and messaging API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update local OpenClaw cron configuration and send messages to configured channels.] <br>

## Skill Version(s): <br>
1.0.8 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
