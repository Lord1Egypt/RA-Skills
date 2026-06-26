## Description: <br>
Automated Binance Futures USDT-M scalping bot using RSI, EMA, volume, Bollinger Bands, auto stop-loss/take-profit handling, Telegram alerts, and health monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mail-eth](https://clawhub.ai/user/mail-eth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to configure and run automated Binance Futures USDT-M trading cycles, including scalping, mean-reversion, notifications, and operational checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact is a real Binance futures trading bot and may place live market orders when run with valid credentials. <br>
Mitigation: Use a dedicated restricted Binance API key with withdrawals disabled, IP allowlisting where available, and no live funds until dry-run or testnet controls and explicit risk limits are added. <br>
Risk: Credential and notification setup can expose sensitive API keys or send trade information to the wrong Telegram destination. <br>
Mitigation: Store credentials only in local environment files, verify the Telegram bot and chat ID before use, and rotate keys if they are exposed. <br>
Risk: The QA runner invokes the trading cycle script instead of the QA audit script, so scheduled QA could trigger live trading. <br>
Mitigation: Fix run_qa.sh to invoke qa_audit.py and review cron entries before enabling automated execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mail-eth/crypto-scalper-bot) <br>
- [Publisher profile](https://clawhub.ai/user/mail-eth) <br>
- [Artifact README](artifact/README.md) <br>
- [Binance](https://www.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, and environment-file configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Binance and optional Telegram credentials; live trading behavior should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
