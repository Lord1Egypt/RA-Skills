## Description: <br>
Track, categorize, and analyze personal expenses from receipts, bank statements, manual entries, CSV imports, budgets, and spending reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to log personal or business expenses, scan receipts, import bank-statement CSVs, set budgets, and produce spending reports. It is intended for local expense tracking where users are comfortable storing financial records on their own machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt and bank-statement-derived transaction data can include sensitive financial records stored locally under ~/.expense-tracker/ or exported CSV files. <br>
Mitigation: Protect that local directory and exported CSVs as private financial records, import only needed fields, and delete or secure files when they are no longer needed. <br>
Risk: Receipt OCR and CSV column mapping can create incorrect transaction records or categories. <br>
Mitigation: Review scanned and imported transactions before relying on reports or budget summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eternal0404/eternal-expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands; local outputs include terminal reports plus JSON and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores transactions, budgets, and categories under ~/.expense-tracker/ and can export transaction data to CSV.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
