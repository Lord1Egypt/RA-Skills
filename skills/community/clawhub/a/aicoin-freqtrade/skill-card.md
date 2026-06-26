## Description: <br>
Helps agents create, backtest, tune, deploy, and monitor Freqtrade crypto strategies using AiCoin data and Freqtrade daemon/API controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[procaross](https://clawhub.ai/user/procaross) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and crypto-bot operators use this skill to manage Freqtrade workflows, including strategy generation, backtesting, hyperopt, strategy and pair switching, dry-run/live mode changes, and bot status, balance, position, and P&L checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live-trading controls can switch modes or place, exit, cancel, or delete real crypto trading actions. <br>
Mitigation: Keep dry_run enabled until intentionally ready for real trading, and require manual confirmation before live-mode, force-enter, force-exit, cancel, or delete actions. <br>
Risk: The skill handles sensitive trading and AiCoin credentials. <br>
Mitigation: Run it only in an environment intended for this bot, avoid unrelated secrets, and do not expose API keys or daemon credentials in chat output. <br>
Risk: Host-mode deployment can install software, write plaintext credentials, and start a persistent trading daemon. <br>
Mitigation: Review host-mode deployment steps before use and restrict execution to machines where persistent Freqtrade operation is intended. <br>


## Reference(s): <br>
- [AiCoin Open Data](https://www.aicoin.com/opendata) <br>
- [AiCoin Open API v3 Catalog](https://open.aicoin.com/api/v3/_catalog) <br>
- [ClawHub Skill Page](https://clawhub.ai/procaross/aicoin-freqtrade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and Python strategy code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue local Node.js script commands against Freqtrade and write strategy or configuration files when authorized.] <br>

## Skill Version(s): <br>
3.5.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
