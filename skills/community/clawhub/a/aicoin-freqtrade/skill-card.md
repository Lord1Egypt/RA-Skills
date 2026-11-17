## Description:

Helps agents create, backtest, tune, deploy, and operate Freqtrade strategies with AiCoin market data integrations across CoinClaw-style agent containers and host-mode environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[procaross](https://clawhub.ai/user/procaross)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-bot operators use this skill to generate and manage Freqtrade strategies, run backtests and hyperopt, switch strategies or trading pairs, and query live bot status, balances, positions, and profit/loss. It is intended for users who understand the risks of automated cryptocurrency trading and can review generated strategy files before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a Freqtrade bot and may interact with configured exchange credentials, which can lead to real trading losses if used in live mode.

Mitigation: Start in dry-run mode, verify exchange credentials and balances separately, and require explicit confirmation before live-mode or manual open/close actions.

Risk: Generated or modified strategy files can affect automated trading behavior.

Mitigation: Review strategy code and configuration changes before deployment, then backtest or dry-run before allowing live trading.

Risk: Crafted action parameters or host-mode setup paths can run unintended commands or code.

Mitigation: Avoid untrusted action inputs, prefer the managed CoinClaw daemon path, and install host prerequisites independently instead of relying on host-mode auto-install.

Risk: Pointing AICOIN_BASE_URL at a non-AiCoin host can redirect API traffic and credentials.

Mitigation: Keep AICOIN_BASE_URL unset or set only to an AiCoin-controlled endpoint.

## Reference(s):

- [AiCoin Open Data](https://www.aicoin.com/opendata)
- [AiCoin Open API v3 Catalog](https://open.aicoin.com/api/v3/_catalog)
- [ClawHub skill page](https://clawhub.ai/procaross/skills/aicoin-freqtrade)
- [Publisher profile](https://clawhub.ai/user/procaross)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON parameters, and generated Python strategy code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Freqtrade strategy and configuration files when used by an agent with filesystem and command execution access.]

## Skill Version(s):

3.5.4 (source: ClawHub release evidence; artifact package.json reports 3.5.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
