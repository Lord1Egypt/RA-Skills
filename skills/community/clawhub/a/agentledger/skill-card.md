## Description: <br>
AgentLedger helps AI agents log purchases, set budgets, generate spending reports, manage multi-currency local ledgers, import Privacy.com card exports, and export CSV or JSON records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-goro](https://clawhub.ai/user/c-goro) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use AgentLedger to maintain a local financial audit trail for agent-made purchases, budgets, accounts, reports, and exports. It is intended for tracking operational expenses such as API credits, subscriptions, infrastructure, tools, and Privacy.com card imports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ledger files, backups, Privacy.com imports, and CSV/JSON exports can contain sensitive financial records. <br>
Mitigation: Store them only in intended local workspace paths, restrict access as appropriate, and avoid recording card numbers, passwords, or unnecessary receipt content. <br>
Risk: Imports and exports read from or write to user-provided file paths. <br>
Mitigation: Check import and export paths before running commands, and review exported files before sharing or moving them outside the workspace. <br>
Risk: The reviewed artifact layout does not match all documented src/ command paths. <br>
Mitigation: Verify the installed package paths before relying on documented commands or script entry points. <br>


## Reference(s): <br>
- [ClawHub AgentLedger listing](https://clawhub.ai/c-goro/agentledger) <br>
- [OpenClaw Documentation](https://openclaw.ai) <br>
- [Privacy.com](https://privacy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files, CSV files] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell commands; ledger records are local JSON files with optional CSV or JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Stores transactions, accounts, budgets, settings, backups, imports, and exports in local workspace paths.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
