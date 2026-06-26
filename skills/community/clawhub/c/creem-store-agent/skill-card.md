## Description: <br>
AI-powered Creem store monitor - alerts, churn analysis, autonomous actions via Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[malakhov-dmitrii](https://clawhub.ai/user/malakhov-dmitrii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SaaS operators use this skill to monitor Creem store webhooks, send Telegram alerts, analyze churn events, and take retention actions such as discounts or subscription pauses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI decisions can automatically create Creem discounts or pause subscriptions before a person reviews them. <br>
Mitigation: Disable or patch auto-execution for live stores unless the operator intentionally accepts automated billing and subscription changes. <br>
Risk: The skill uses Creem, Telegram, and Anthropic credentials and may process customer or subscription information through those services. <br>
Mitigation: Use test or least-privileged Creem credentials, restrict the Telegram chat, and review Anthropic and Telegram data-sharing implications before deployment. <br>
Risk: Telegram inline actions can trigger customer retention changes. <br>
Mitigation: Limit bot access to trusted operators and verify the target chat before enabling live actions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/malakhov-dmitrii/creem-store-agent) <br>
- [Creem](https://creem.io) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Build tutorial](https://dev.to/hennessy811/building-an-ai-agent-that-saves-your-saas-revenue-nkf) <br>
- [Demo video](https://youtube.com/shorts/M9A876D5JEE) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Telegram messages, Markdown documentation, inline shell commands, configuration values, and Creem API actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Creem, Telegram, and Anthropic credentials for the full live workflow; can fall back to rule-based churn decisions when Anthropic is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
