## Description:

Runs a local, free checker for elevator maintenance and annual-inspection ledgers, covering six table-level consistency checks and returning findings with source line numbers and original text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External property managers, elevator administrators, safety staff, and operations teams use this skill to check elevator maintenance and annual-inspection ledgers for date, count, duplicate-entry, total-row, and required-field issues. It is advisory and checks ledger text only, not real-world maintenance work or regulatory databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat ledger checks as proof of real-world elevator compliance.

Mitigation: Use the output as an advisory ledger consistency check and have qualified personnel review original records, site conditions, and applicable regulatory requirements.

Risk: The skill checks pasted or JSON ledger text only and does not read original XLSX/PDF files or verify regulatory databases.

Mitigation: Provide complete ledger text with the required columns and separately validate source files, certificates, and inspection records.

Risk: The free edition omits rescue-time, missing-item, fault-closure, vendor-qualification, and grouped-rollup checks.

Mitigation: Review the reported checks_not_run and checks_out_of_scope fields and run additional review for omitted safety or compliance categories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/elevator-maintenance-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON findings with summaries, executed-check lists, and source evidence fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, category, source line, elevator identifier, message, original line text, numeric difference where applicable, and advice.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter is 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
