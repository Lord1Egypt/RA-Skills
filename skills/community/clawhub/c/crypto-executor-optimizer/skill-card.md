## Description: <br>
Autonomous optimizer skill for Wesley that reads Binance trading performance every 6 hours, analyzes win rate and strategy metrics, and tunes executor.py parameters through backup, modification, validation, and restart steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators of the crypto-executor bot use this skill to review trading performance and apply bounded parameter changes to executor.py on a recurring schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change a live crypto trading bot and restart the trading service. <br>
Mitigation: Use paper trading or a small restricted account first, and review each proposed optimization before allowing recurring execution. <br>
Risk: Setup can store Binance credentials and use them when the bot restarts. <br>
Mitigation: Disable withdrawals on exchange keys, prefer a secret manager where available, and restrict local credential file permissions. <br>
Risk: Setup can download executable trading code from moving GitHub branch URLs. <br>
Mitigation: Audit the downloaded code and pin reviewed commits before running it. <br>
Risk: Cron, sudo, and process restart permissions can expand operational impact. <br>
Mitigation: Review crontab and sudo permissions before installation and remove the scheduled job when the optimizer is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/crypto-executor-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/georges91560) <br>
- [External executor.py download](https://raw.githubusercontent.com/georges91560/crypto-executor/main/executor.py) <br>
- [External crypto_oracle.py download](https://raw.githubusercontent.com/georges91560/crypto-sniper-oracle/main/crypto_oracle.py) <br>
- [Telegram Bot API endpoint pattern](https://api.telegram.org/bot*) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and parameter values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger file backups, executor.py parameter updates, logs, cron setup, and service restarts when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
