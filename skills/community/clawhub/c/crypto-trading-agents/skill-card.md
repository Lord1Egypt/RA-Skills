## Description:

Crypto Trading Agents helps agents set up and use a TradingAgents-based multi-agent crypto analysis and Binance spot-trading workflow with technical, news, sentiment, and fundamentals analysis, trading-signal generation, and optional order execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kriouerlia](https://clawhub.ai/user/kriouerlia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure and operate a crypto quantitative-trading assistant for strategy research, market analysis, and Binance spot-trading workflows. It can guide analysis-only use, testnet trials, and optional live order execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable remote installation code and install unpinned trading dependencies.

Mitigation: Use a fresh virtual environment or container, install uv through a trusted pinned method, and pin the external repository and Python dependencies before use.

Risk: The workflow handles Binance exchange keys and can execute spot-market trades.

Mitigation: Start with BINANCE_TESTNET=true and use Binance API keys that cannot withdraw funds.

Risk: Optional WeChat notifications can send trading and account activity to a webhook provider.

Mitigation: Enable WeChat notifications only when that data sharing is acceptable for the deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kriouerlia/skills/crypto-trading-agents)
- [TradingAgents repository](https://github.com/TauricResearch/TradingAgents.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, environment-variable configuration, analysis commands, and optional Binance execution workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
