## Description: <br>
Bangladesh stock market data and analytics for DSE (Dhaka Stock Exchange), including prices, signals, EMA channels, and Fibonacci levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rashed-mamoon](https://clawhub.ai/user/rashed-mamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query Bangladesh Dhaka Stock Exchange market data, news, price history, technical indicators, and trading analytics through the StockAI Live API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a StockAI API key to stock-ai.live and may access portfolio data tied to that account. <br>
Mitigation: Install only if you trust stock-ai.live, keep STOCKAI_API_KEY secret, and avoid committing .env or agent config files that contain credentials. <br>
Risk: A portfolio command exists but is not clearly disclosed in the main instructions. <br>
Mitigation: Limit use to expected commands unless portfolio access is intended, and review any portfolio output before sharing it. <br>
Risk: Command outputs can include promotional signup or upgrade content. <br>
Mitigation: Review generated JSON before relaying it to users, especially when neutral market-data output is expected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rashed-mamoon/bd-stock-live) <br>
- [StockAI Live](https://stock-ai.live) <br>
- [StockAI Live Documentation](https://stock-ai.live/docs) <br>
- [StockAI Live API Keys](https://stock-ai.live/api-keys) <br>
- [StockAI Live Pricing](https://stock-ai.live/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Analysis] <br>
**Output Format:** [Markdown guidance with shell commands; command output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STOCKAI_API_KEY. Some command responses include promotional signup or upgrade content.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
