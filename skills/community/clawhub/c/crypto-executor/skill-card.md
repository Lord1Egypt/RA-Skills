## Description:

Crypto Executor is an autonomous Binance spot-trading agent that monitors markets, sizes positions, places market and OCO orders, sends Telegram alerts, and writes trading state and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to install, configure, and run a Binance spot-trading bot with live API credentials, risk limits, optional Telegram alerts, and optional oracle-assisted market signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can autonomously trade real funds using live Binance credentials.

Mitigation: Use paper trading or testnet first, start with limited capital, disable withdrawals, IP-allowlist API keys, and monitor trading activity before any live deployment.

Risk: The skill depends on live credentials and can send alerts through Telegram.

Mitigation: Store secrets in a locked-down credentials file or environment manager, avoid sourcing them into a general shell, rotate exposed keys, and keep Telegram tokens optional unless alerts are required.

Risk: The optional oracle integration executes external code as a subprocess.

Mitigation: Audit the oracle code before installation, pin exact commits and package versions, and run the bot in an isolated virtual environment.

Risk: Systemd or cron persistence can keep autonomous trading active after reboot or failure.

Mitigation: Do not enable persistence until the executor and oracle have been reviewed and the operator has accepted live trading risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/crypto-executor)
- [Publisher profile](https://clawhub.ai/user/georges91560)
- [crypto-sniper-oracle external dependency](https://github.com/georges91560/crypto-sniper-oracle)
- [Binance REST API endpoint](https://api.binance.com/api/v3/*)
- [Binance WebSocket stream endpoint](wss://stream.binance.com:9443/ws/*)
- [Telegram Bot API endpoint](https://api.telegram.org/bot*)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python code, environment variables, and generated JSON/text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Binance API credentials; can use Telegram credentials for alerts; writes portfolio, position, trade-history, performance, learned-configuration, alert, and daily-report files under /workspace.]

## Skill Version(s):

2.3.4 (source: server release metadata; artifact frontmatter reports 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
