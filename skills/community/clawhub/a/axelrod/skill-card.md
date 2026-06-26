## Description: <br>
AI-powered Base-chain trading and on-chain query agent via natural language. Use when the user wants to trade crypto (buy/sell/swap tokens), set up automated strategies (DCA, limit orders, RSI), check portfolio balances, view token prices, query token info/analysis, check order status, manage take-profit/stop-loss orders, or ask about crypto/DeFi topics on Base chain. Always run scripts/axelrod_chat.py to fetch real-time results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aixvcteam](https://clawhub.ai/user/aixvcteam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Axelrod to connect an OpenClaw agent to AIxVC for Base-chain token trading, portfolio and price queries, order management, and automated trading strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real crypto funds on Base and some small orders may execute without a separate confirmation step. <br>
Mitigation: Use limited credentials where available, start with small orders, avoid broad auto-routing for general crypto discussion, and review trade details before execution. <br>
Risk: The skill depends on AIxVC API credentials with authority to query and trade. <br>
Mitigation: Store AK/SK credentials only in the agent environment configuration, do not share or commit them, and rotate or revoke credentials if exposed. <br>


## Reference(s): <br>
- [Axelrod API Reference](references/api.md) <br>
- [AIxVC AI Automation](https://aixvc.io/chat) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Axelrod Skill Page](https://clawhub.ai/aixvcteam/axelrod) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command examples and human-readable CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction status, balances, token prices, order details, confirmation keys, or error messages returned by the AIxVC API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
