## Description: <br>
Btc Strategy V40 provides a multi-factor BTC-USDT-SWAP trading strategy using EMA, RSI, momentum, market sentiment, and risk controls for Agent Trade Kit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianzhentao1](https://clawhub.ai/user/qianzhentao1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate BTC-USDT-SWAP trading signals and produce order, position sizing, stop-loss, and monitoring guidance for OKX-oriented trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an automated leveraged crypto-trading setup with real account-impacting authority. <br>
Mitigation: Run it first in paper mode or with a limited test exchange account, require manual approval before live orders, and enforce independent leverage and notional limits. <br>
Risk: The monitor includes under-disclosed external Telegram notification behavior. <br>
Mitigation: Remove or reconfigure the Telegram token and chat settings before running the monitor. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qianzhentao1/btc-strategy-v40) <br>
- [OKX market ticker endpoint](https://www.okx.com/api/v5/market/ticker?instId=BTC-USD) <br>
- [Binance BTCUSDT price endpoint](https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT) <br>
- [Telegram Bot sendMessage endpoint](https://api.telegram.org/bot$BOT_TOKEN/sendMessage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live trading actions, monitoring state, and external notification behavior that should be reviewed before execution.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata; artifact frontmatter reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
