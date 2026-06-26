## Description: <br>
Automates bookkeeping workflows including EÜR preparation, DATEV CSV export, PDF receipt analysis, invoice generation, and tax preparation support for freelancers and small businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akkualle](https://clawhub.ai/user/akkualle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as freelancers and small businesses use this skill to analyze receipts, categorize bookkeeping entries, create EÜR reports, export DATEV-compatible CSV files, and draft invoices for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports under-disclosed invoice-generation scripts with hard-coded company, tax, and bank details. <br>
Mitigation: Review the scripts and replace all embedded company, tax, and bank details before generating invoices. <br>
Risk: The security guidance warns that DATEV command behavior can write financial files unexpectedly. <br>
Mitigation: Run DATEV exports only against intended input and output paths, preferably on copies of bookkeeping data. <br>
Risk: The security guidance states that tax and accounting outputs are drafts. <br>
Mitigation: Have EÜR, DATEV, invoice, and tax-preparation outputs reviewed by a qualified professional before filing or business use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akkualle/akkualle-accounting-assistant) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/akkualle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts that produce JSON, CSV, Markdown reports, and PDF invoice files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be treated as accounting drafts that require review before use with real business records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
