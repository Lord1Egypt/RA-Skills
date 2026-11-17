## Description:

Bybit AI Trading Skill - Trade on Bybit using natural language. Covers spot, derivatives, earn, and more. Works with Claude, ChatGPT, OpenClaw, and any AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorwu-bybit](https://clawhub.ai/user/victorwu-bybit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an AI assistant retrieve Bybit market data, configure credentials, and prepare or execute supported Bybit trading, account, earn, bot, copy trading, fiat, on-chain, and TradFi workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an assistant to place real-money trades and persist OAuth or API credentials.

Mitigation: Use a dedicated Bybit subaccount with limited balance, Read+Trade permissions only, no Withdraw permission, and Testnet first before any Mainnet use.

Risk: The security summary says the skill can automatically replace its own files from mutable remote sources.

Mitigation: Review or disable auto-update and module-fetch behavior before using Mainnet, and verify fetched content integrity before trusting updated modules.

Risk: Some financial workflows are described as under-scoped in the security summary.

Mitigation: Require separate human confirmations for transfers, bot creation, account-admin changes, and other state-changing operations; inspect the operation summary before execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/victorwu-bybit/skills/bybit-exchange-trading-skill)
- [Bybit AI Subaccount help article](https://www.bybit.com/en/help-center/article/Introduction-to-the-AI-Subaccount)
- [Bybit website](https://www.bybit.com)
- [Bybit TradFi Integration docs](https://bybit-exchange.github.io/docs/v5/tradfi-integration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands, API request examples, confirmation cards, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bybit API endpoint examples, masked credential displays, environment setup instructions, and user confirmation prompts for mainnet write operations.]

## Skill Version(s):

1.5.3 (source: server release metadata; artifact frontmatter reports 1.5.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
