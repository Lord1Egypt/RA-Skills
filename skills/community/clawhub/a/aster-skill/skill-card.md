## Description:

Monitors BTC, ETH, SOL, and BNB news, classifies market sentiment with an LLM, and can place leveraged long or short orders on Aster with stop-loss, take-profit, and cooldown controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterskillagent](https://clawhub.ai/user/asterskillagent)

### License/Terms of Use:


## Use Case:

Crypto trading agents and operators can use this skill to monitor recent crypto news and convert high-confidence sentiment signals into Aster orders for BTC, ETH, SOL, and BNB. Because it can trade leveraged assets automatically, it should be deployed only with explicit trading safeguards and account limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place leveraged real-money crypto trades automatically from LLM-classified news.

Mitigation: Use paper trading by default and require explicit approval for each live trade unless the deployment has separately approved autonomous trading.

Risk: Automated market orders can create unintended loss exposure during volatile or low-quality news events.

Mitigation: Enforce strict position sizing, loss limits, cooldowns, and exchange-side keys with withdrawals disabled.

Risk: News content is sent to OpenAI for sentiment analysis.

Mitigation: Disclose the external processing path and avoid submitting confidential or restricted data through the news-analysis workflow.

Risk: Runtime behavior depends on external packages and an OpenNews MCP integration.

Mitigation: Pin and review dependencies, verify the MCP installation source, and scan the release before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asterskillagent/skills/aster-skill)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration]

**Output Format:** [Scheduled execution with exchange API calls, console logs, and JSON sentiment analysis responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Aster API credentials, an OpenAI API key, and OpenNews MCP integration; default configuration watches BTC, ETH, SOL, and BNB every five minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
