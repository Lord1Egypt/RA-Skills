## Description: <br>
Generates Word (.docx) reports and Excel (.xlsx) workbooks as downloadable files for SMSF, accounting, compliance, and business document workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mysmsf](https://clawhub.ai/user/mysmsf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, accountants, and business operators use this skill to generate draft SMSF reports, trustee summaries, checklists, budgets, invoices, and simple spreadsheet workbooks that require review before client or regulatory use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SMSF, accounting, or compliance documents may be mistaken for final professional advice or regulator-ready material. <br>
Mitigation: Treat generated documents as drafts and have a qualified accountant, auditor, or adviser review them before client or regulatory use. <br>
Risk: Local file generation can write to unintended locations or replace existing files when output paths or --force are used incorrectly. <br>
Mitigation: Choose explicit safe output locations and use --force only when the user intends to replace an existing file. <br>
Risk: Unpinned package dependencies may reduce reproducibility or introduce supply-chain exposure. <br>
Mitigation: Install dependencies only from trusted package sources and pin versions when reproducible builds are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mysmsf/docx-xlsx-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [DOCX and XLSX files generated from command-line arguments or JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local .docx and .xlsx files; existing output files are not overwritten unless --force is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
