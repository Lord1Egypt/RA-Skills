## Description: <br>
Modular prediction market trading platform for OpenClaw bots. Trade on Polymarket, manage wallets, transfer USDC, and automate trading strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stonega](https://clawhub.ai/user/stonega) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent create and manage wallets, monitor balances and positions, and trade prediction markets such as Polymarket through the Clawearn CLI. <br>

### Deployment Geography for Use: <br>
Global, subject to user eligibility, market availability, and prediction-market jurisdiction restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage real funds through wallets, transfers, approvals, deposits, withdrawals, and trades. <br>
Mitigation: Install only when an agent is intentionally authorized to manage real funds, use a fresh low-balance hot wallet, and require manual approval for transfers, withdrawals, trades, cancellations, and token approvals. <br>
Risk: The installer and skill-update flows fetch executable or operational content over curl-based commands. <br>
Mitigation: Avoid curl-to-bash installation unless independently verified, pin or review fetched files before use, and disable automatic self-updates. <br>
Risk: Private keys or credentials may be exposed through visible command lines, logs, files, or agent messages. <br>
Mitigation: Do not echo or pass private keys in visible command lines; store secrets in dedicated credential storage with restrictive file permissions and redact sensitive output. <br>
Risk: Trading automation can create financial losses through incorrect markets, stale orders, or excessive exposure. <br>
Mitigation: Start with small balances, configure position and exposure limits, review market details before orders, monitor open orders, and require human approval for large trades. <br>


## Reference(s): <br>
- [Claw Earn ClawHub page](https://clawhub.ai/stonega/clawearn) <br>
- [Clawearn homepage](https://clawearn.xyz) <br>
- [Clawearn documentation](https://docs.clawearn.xyz) <br>
- [Polymarket documentation](https://docs.polymarket.com) <br>
- [Polymarket homepage](https://www.polymarket.com) <br>
- [Artifact README](artifact/README.md) <br>
- [Main skill definition](artifact/SKILL.md) <br>
- [Wallet management guide](artifact/core/wallet/SKILL.md) <br>
- [Security best practices](artifact/core/security/SKILL.md) <br>
- [Polymarket trading skill](artifact/markets/polymarket/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide wallet creation, transfers, token approvals, deposits, withdrawals, order placement, order cancellation, balance checks, and monitoring actions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
