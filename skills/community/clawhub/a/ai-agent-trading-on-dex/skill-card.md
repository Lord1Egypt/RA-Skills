## Description: <br>
Backtest and deploy trading strategies on Superior Trade's managed cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmmmssss8899](https://clawhub.ai/user/mmmmssss8899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading users use this skill to turn trading ideas into backtests, review results, and create user-confirmed live deployments on Superior Trade for Hyperliquid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required API key can create and manage backtests and deployments, including deployments that execute live trades. <br>
Mitigation: Store SUPERIOR_TRADE_API_KEY only in an environment or credential manager, keep .env files out of git, and require explicit user confirmation before creating or starting live deployments. <br>
Risk: Automated crypto trading can lose money even when configured correctly. <br>
Mitigation: Backtest strategies first, review the resulting metrics, start with conservative stake sizes, and avoid treating backtest performance as a guarantee. <br>
Risk: Wallet or exchange credential misuse could expose funds or sensitive account access. <br>
Mitigation: Never request, log, store, or transmit private keys or seed phrases, and never enable withdrawal permissions on exchange API keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmmmssss8899/ai-agent-trading-on-dex) <br>
- [Superior Trade account homepage](https://account.superior.trade) <br>
- [Superior Trade API documentation](https://api.superior.trade/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with API request guidance, JSON configuration snippets, and Python strategy code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPERIOR_TRADE_API_KEY; live deployment actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
3.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
