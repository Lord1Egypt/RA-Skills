## Description: <br>
Track AI agent earnings, tasks, and payments. Use when logging completed work, checking balance, viewing payment history, or generating invoices. Supports crypto (USDC/ETH) and fiat tracking with running totals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and CLI-based agents use Agent Ledger to record completed work, track pending and paid balances, store an optional wallet address, and export ledger data for reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ledger files, exports, and wallet settings can contain task descriptions, payment amounts, payment status, and an optional wallet address. <br>
Mitigation: Treat ~/.agent-ledger and exported JSON or CSV files like financial records; restrict access and share exports only with intended recipients. <br>
Risk: A task can be marked paid before the user has verified the corresponding payment. <br>
Mitigation: Review ledger entries and payment records before running the pay command. <br>


## Reference(s): <br>
- [Agent Ledger on ClawHub](https://clawhub.ai/rogue-agent1/agent-ledger) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands, configuration] <br>
**Output Format:** [CLI text output, JSON Lines ledger entries, CSV exports, and local JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local ledger and configuration files under ~/.agent-ledger by default; AGENT_LEDGER_DIR can override the storage directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
