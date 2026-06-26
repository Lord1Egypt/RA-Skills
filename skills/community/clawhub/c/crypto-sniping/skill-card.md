## Description: <br>
Automated Binance bot using RSI, MACD, volume spikes, and whale tracking to generate signals, execute trades, and manage risk on BTC, ETH, and SOL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or technically skilled traders use this skill to configure and run a Binance trading bot that scans markets, sends alerts, and can execute paper or live trades with position sizing and loss limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place automated trades that affect real funds. <br>
Mitigation: Start in paper or read-only mode, verify symbols, position sizing, and daily loss limits, and enable live mode only after accepting the trading risk. <br>
Risk: The skill requires sensitive Binance credentials and may use Telegram notification credentials. <br>
Mitigation: Use narrowly scoped Binance keys with withdrawals disabled, protect environment variables, and verify the Telegram destination before running alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorjenorbulim/crypto-sniping) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, YAML configuration examples, and Python code behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Binance and optional Telegram credentials; paper mode is the safer default, while live mode can place real trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
