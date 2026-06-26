## Description: <br>
Complete autonomous trading engine for Binance with WebSocket real-time market data, OCO orders, Kelly Criterion position sizing, trailing stops, circuit breakers, daily performance reports, adaptive strategy mixing, memory persistence, and performance alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, and run an autonomous Binance spot-trading agent with credential setup, runtime supervision, reporting, and risk controls. It is intended for users who deliberately want agent-managed real-money trading and can supervise the system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place autonomous real-money Binance orders. <br>
Mitigation: Use a dedicated Binance API key with withdrawals, transfers, margin, and futures disabled; restrict the key by IP; start on testnet or with a very small balance; and supervise behavior before increasing exposure. <br>
Risk: The executor can persist across reboots when installed as a service. <br>
Mitigation: Delay systemd auto-start until supervised runs are understood, and keep documented stop and disable commands available before deployment. <br>
Risk: The optional oracle helper is external code executed by subprocess. <br>
Mitigation: Audit the helper dependency, pin it to a reviewed commit or tag, and install it only when the additional signal source is required. <br>
Risk: Telegram alerts may expose operational trading details if bot credentials or chats are shared. <br>
Mitigation: Keep Telegram optional, private, and credential-scoped; rotate bot tokens if chat access changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/crypto-executor) <br>
- [Publisher profile](https://clawhub.ai/user/georges91560) <br>
- [crypto-sniper-oracle external dependency](https://github.com/georges91560/crypto-sniper-oracle) <br>
- [Binance REST API endpoint pattern](https://api.binance.com/api/v3/*) <br>
- [Binance WebSocket stream endpoint pattern](wss://stream.binance.com:9443/ws/*) <br>
- [Telegram Bot API endpoint pattern](https://api.telegram.org/bot*) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, Python code, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, configuration, operating, monitoring, and risk-management guidance for a Python trading executor.] <br>

## Skill Version(s): <br>
2.3.4 (source: server release metadata; artifact frontmatter reports 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
