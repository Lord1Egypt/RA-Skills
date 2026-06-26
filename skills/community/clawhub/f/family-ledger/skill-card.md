## Description: <br>
Family Ledger helps a household record, query, and summarize daily expenses, social gift records, loans, and reimbursements in shared JSON ledger files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liumeixin](https://clawhub.ai/user/liumeixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External household users use this skill to maintain a family ledger across daily income and expenses, social gift exchanges, loans, and reimbursements. It guides entries into local JSON files and supports lookups and summaries by date, category, person, status, child, or property. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores household finance details and user identity mappings in shared local JSON files. <br>
Mitigation: Restrict access to ~/.openclaw/workspace/shared/ledger/ and avoid recording sensitive details that are not needed for bookkeeping. <br>
Risk: Ledger entries, loan status, reimbursement status, or summaries may be incorrect when a command is ambiguous or a file is overwritten incorrectly. <br>
Mitigation: Review ambiguous entries before accepting them, keep versioned backups of the JSON ledger files, and verify loan and reimbursement status changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liumeixin/family-ledger) <br>
- [Publisher profile](https://clawhub.ai/user/liumeixin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown guidance with JSON ledger updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local ledger records for shared JSON files under ~/.openclaw/workspace/shared/ledger/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
