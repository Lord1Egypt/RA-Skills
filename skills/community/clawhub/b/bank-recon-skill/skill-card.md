## Description: <br>
Bank Recon Skill reconciles bank statement PDF or Excel files against general ledger workbooks and generates an Excel workbook with matched, unreconciled, and summary tabs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChipmunkRPA](https://clawhub.ai/user/ChipmunkRPA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accountants, finance teams, and agents supporting them use this skill to compare bank activity with GL transactions, identify matched and unmatched records, and prepare reviewable reconciliation workbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank and ledger inputs and generated reconciliation workbooks can contain sensitive financial information. <br>
Mitigation: Process only files suitable for local handling, choose output paths deliberately, avoid shared or synced folders when inappropriate, and delete generated workbooks when they are no longer needed. <br>
Risk: PDF inputs create an additional extracted workbook beside the original statement. <br>
Mitigation: Account for the companion '_extracted.xlsx' file when selecting directories and cleaning up generated financial data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance, shell command invocation, terminal summary text, and generated .xlsx workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a reconciliation workbook and, for PDF bank statements, a companion extracted workbook next to the PDF input.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
