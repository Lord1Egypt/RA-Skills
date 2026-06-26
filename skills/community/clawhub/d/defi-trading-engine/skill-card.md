## Description: <br>
DeFi Trading Engine - Autonomous DeFi trading bot with self-improving review system for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avmw2025](https://clawhub.ai/user/avmw2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to configure and run an agent-assisted DeFi trading workflow that scans tokens, checks risk limits, executes Bankr trades, logs activity, and reviews performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live crypto trades through Bankr, exposing funds to loss or unintended execution. <br>
Mitigation: Use a separate low-balance wallet, run explicit dry-run tests first, and require human approval for every live trade. <br>
Risk: Wallet configuration and Bankr credentials may be sensitive. <br>
Mitigation: Protect ~/.bankr/config.json, avoid committing secrets or wallet material, and verify the Bankr CLI source before use. <br>
Risk: Scheduled automation can continue scanning or trading after the operator loses context. <br>
Mitigation: Avoid enabling cron jobs until the stop procedure is understood and monitor or disable scheduled runs when not actively supervising the workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/avmw2025/defi-trading-engine) <br>
- [Bankr setup guide](references/bankr-setup.md) <br>
- [Trading strategies](references/strategies.md) <br>
- [CoinGecko API documentation](https://www.coingecko.com/en/api/documentation) <br>
- [Base Chain documentation](https://docs.base.org) <br>
- [Bankr](https://bankr.bot) <br>
- [BaseScan](https://basescan.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local trading logs, reviews, and candidate-token JSON when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
