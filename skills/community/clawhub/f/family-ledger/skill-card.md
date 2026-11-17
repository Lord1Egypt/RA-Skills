## Description:

Family Ledger helps a household record, query, and summarize daily expenses, social-gift exchanges, loans, and reimbursements in shared JSON ledgers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumeixin](https://clawhub.ai/user/liumeixin)

### License/Terms of Use:

MIT-0

## Use Case:

Household members use this skill to add, query, and summarize family ledger entries for daily income and expenses, social-gift records, loans, and reimbursements. It supports shared bookkeeping where entries may be attributed to mapped household users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores shared household financial records and identity mappings on disk.

Mitigation: Use it only in a trusted household or workspace, remove real personal identifiers from the package, and restrict permissions on the ledger directory.

Risk: The skill does not define clear privacy or authorization boundaries for writes or cross-user queries.

Mitigation: Require explicit confirmation and authorization before allowing ledger writes, status changes, or queries across mapped users.

Risk: Ledger updates are implemented by reading and overwriting JSON files, which can lose or corrupt records if changes are not reviewed.

Mitigation: Review proposed JSON changes before execution and keep backups or change history for shared ledger files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liumeixin/skills/family-ledger)
- [Publisher profile](https://clawhub.ai/user/liumeixin)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Natural-language responses and JSON ledger records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains daily, social-gift, loan, reimbursement, and user-mapping ledger data in shared JSON files.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
