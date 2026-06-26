## Description: <br>
Provides Binance spot and futures account queries and trading workflows, including balances, positions, orders, stop-loss and take-profit commands, and PnL checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hybrid1labs](https://clawhub.ai/user/hybrid1labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect Binance account state, retrieve prices, and prepare or execute spot and futures trading actions through Binance APIs. It is intended for users who deliberately want an agent-assisted Binance workflow and can review financial actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Binance futures orders, close positions, change exposure, and set stop-loss or take-profit orders, including leveraged trades with real funds. <br>
Mitigation: Require separate human confirmation before any order, cancellation, leverage change, stop-loss, take-profit, or position close; prefer testnet or read-only credentials unless live trading is explicitly required. <br>
Risk: Binance API keys and secrets are needed for authenticated requests and could expose account access if copied into chats, logs, files, or command output. <br>
Mitigation: Use restricted, revocable Binance API keys with withdrawals disabled, apply IP restrictions where possible, and keep credentials out of shared prompts, screenshots, logs, and repository files. <br>
Risk: The artifact declares broad automatic activation and the security summary notes no enforced confirmation safeguards. <br>
Mitigation: Invoke the skill only when Binance account access is intended, disable broad auto-invocation where possible, and review generated commands and parameters before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hybrid1labs/binance-pro-hybrid) <br>
- [Binance API documentation](https://binance-docs.github.io/apidocs/) <br>
- [Binance testnet](https://testnet.binance.vision/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Binance API credentials from environment variables or ~/.openclaw/credentials/binance.json and can call live Binance APIs when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
