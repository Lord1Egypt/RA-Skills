## Description: <br>
BudgetRcd helps agents record personal expenses, check remaining budgets, query spending, and apply weekday/weekend budget rules with dynamic carry-forward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kazuya-ecnu](https://clawhub.ai/user/kazuya-ecnu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using an agent for personal budgeting use BudgetRcd to record expenses, query daily or monthly spending, check remaining budget, and receive overspend status using configurable weekday and weekend budget rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently create or modify personal finance records. <br>
Mitigation: Review the configured budget data location before use and require confirmation for ambiguous, bulk, update, delete, or receipt-import actions. <br>
Risk: The release security summary says the code does not enforce the storage boundary promised by the documentation. <br>
Mitigation: Validate configured paths before execution and confirm that all writes stay under the approved budget folder. <br>


## Reference(s): <br>
- [BudgetRcd ClawHub page](https://clawhub.ai/kazuya-ecnu/budgetrcd) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, guidance] <br>
**Output Format:** [Natural-language budget summaries plus local JSON budget and expense records, with optional copied receipt image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists expense, budget, pool, and receipt data under the configured budget directory when installed and executed.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
