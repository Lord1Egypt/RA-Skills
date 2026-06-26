## Description: <br>
Act as a personal accountant using the fscl (fiscal) CLI for Actual Budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benbjurstrom](https://clawhub.ai/user/benbjurstrom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to have an agent help manage Actual Budget workflows, including budgeting, bank imports, categorization, transaction rules, spending analysis, and account maintenance through fscl commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial data and can make real Actual Budget changes. <br>
Mitigation: Review proposed changes carefully, use dry-run or draft workflows for imports and bulk edits, and require explicit user approval before applying changes. <br>
Risk: Passing a server password on the command line may expose credentials through shell history or process inspection. <br>
Mitigation: Prefer interactive login or another safer secret flow over using --password on the command line. <br>
Risk: Deletes, merges, month applies, committed rule runs, and server-synced actions may be difficult to reverse. <br>
Mitigation: Explicitly approve deletes, merges, month applies, rules run with --and-commit, and any server-synced changes before execution. <br>


## Reference(s): <br>
- [Actual Budget](https://actualbudget.org/) <br>
- [Budgeting Concepts](references/budgeting.md) <br>
- [Command Reference](references/command-reference.md) <br>
- [Command Cheat Sheet](references/commands.md) <br>
- [Credit Cards](references/credit-cards.md) <br>
- [Importing Transactions](references/import-guide.md) <br>
- [Query Library](references/query-library.md) <br>
- [Transaction Rules](references/rules.md) <br>
- [Workflow: Budget Maintenance](references/workflow-maintenance.md) <br>
- [Workflow: New Budget Onboarding](references/workflow-onboarding.md) <br>
- [Workflow: Budget Optimization](references/workflow-optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with human-readable summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fscl JSON output as evidence for user-facing financial summaries; sensitive actions should be previewed and approved before execution.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
