## Description:

Runs a US bookkeeping cleanup checklist over your ledger, reconciling accounts and listing every uncategorized or duplicate entry left to fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External US bookkeepers, small CPA firm staff, and business owners use it to organize month-end ledger cleanup, reconcile accounts against statements, track unresolved items, and prepare a handover for a tax preparer.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The checklist and text linter cannot verify that balances or transactions are correct.

Mitigation: Independently verify balances against supporting statements and the ledger, and investigate differences before marking reconciliations complete.

Risk: The optional Windows toolkit is a separate unsigned download, and its supplied checksum alone does not establish safety.

Mitigation: The bundled Python workflow does not require the toolkit; assess it separately and only run it if you accept the risks of unsigned software.

## Reference(s):

- [US month-end bookkeeping cleanup](references/bookkeeping-cleanup.md)
- [Bookkeeping Cleanup on ClawHub](https://clawhub.ai/rapidworker1/skills/bookkeeping-cleanup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Markdown cleanup checklist, reconciliation log, open-items list, and handover note, supported by a YAML checklist template.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checklist guidance only; account balances and transaction classifications require independent verification.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
