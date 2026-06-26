## Description: <br>
Use this skill to extract receipt information, record expenses, track budgets, and manage financial receipts using the ClawReceipt CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SakuraKo-IRS](https://clawhub.ai/user/SakuraKo-IRS) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and OpenClaw agents use ClawReceipt to record receipt details, track monthly spending against a budget, list receipt history, and export local financial records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt data, the SQLite database, and exported CSV/XLSX files may contain private financial records. <br>
Mitigation: Store generated data locally in a trusted environment and handle database and export files as private financial records. <br>
Risk: Unpinned Python dependencies can change behavior over time. <br>
Mitigation: Install in a trusted virtual environment and pin dependencies before regular use. <br>
Risk: Receipt fields extracted by an agent can be incomplete or incorrect before they are saved. <br>
Mitigation: Review date, store, amount, category, and optional time values before running the add command. <br>
Risk: The interactive TUI can block an automated agent session. <br>
Mitigation: Use non-interactive add, budget, list, or alert commands for agent workflows and reserve the TUI for manual use. <br>


## Reference(s): <br>
- [ClawReceipt ClawHub Page](https://clawhub.ai/SakuraKo-IRS/clawreceipt) <br>
- [ClawReceipt README](artifact/README.md) <br>
- [ClawReceipt Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite receipt records and CSV or XLSX exports when the corresponding CLI commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
