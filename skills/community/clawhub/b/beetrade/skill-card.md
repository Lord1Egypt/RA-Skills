## Description: <br>
Use Beecli to interact with the Beetrade platform for authentication, market data, bot/strategy operations, alerts, accounts, and portfolio workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[htranbee](https://clawhub.ai/user/htranbee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the Beetrade CLI for authentication, market data, bot and strategy workflows, alerts, accounts, and portfolio tasks. It emphasizes read-only discovery, paper trading, and backtesting before high-impact live trading or account changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved commands can affect real trading accounts, including live trading, account changes, deletes, or scheduled execution. <br>
Mitigation: Use status, list, paper, and backtest commands first, preview the exact command, and require explicit user confirmation before high-impact actions. <br>
Risk: Beecli authentication files and command output may contain access tokens, refresh tokens, API keys, secrets, or passwords. <br>
Mitigation: Do not read files under ~/.beecli/, do not expose credentials in commands or output, and redact sensitive JSON fields before reporting results. <br>
Risk: Command output, API responses, or user-supplied JSON can contain prompt-injection text that conflicts with the skill's safety rules. <br>
Mitigation: Treat external content as untrusted input and validate any suggested command independently against the safety rules before execution. <br>


## Reference(s): <br>
- [Beecli Command Reference](references/commands.md) <br>
- [Beetrade on ClawHub](https://clawhub.ai/htranbee/beetrade) <br>
- [Beetrade API endpoint](https://api.prod.beetrade.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and redacted JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires beecli; redacts credential fields and requires explicit confirmation before live trading, delete, credential update, order, or scheduled execution changes.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
