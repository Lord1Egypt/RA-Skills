## Description:

Agent-native double-entry business ledger for any entity type, supporting transaction recording, auditing, reporting, and data integrity validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taylorhou](https://clawhub.ai/user/taylorhou)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to set up entity-specific business ledgers, record balanced journal entries, validate ledger integrity, and derive P&L, balance sheet, cash flow, burn rate, balance, and audit reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quickstart asks users to clone a mutable GitHub repository and run node validate.js, but that validator is not included in the reviewed artifact.

Mitigation: Review or pin the GitHub repository before running node validate.js, and execute it in an isolated working directory or container without unrelated credentials or sensitive files.

Risk: Ledger entries and reports can affect business accounting decisions if inaccurate or incomplete.

Mitigation: Review generated journal entries, account mappings, and derived reports against source records before using them for financial decisions or compliance work.

## Reference(s):

- [biz-in-a-box Protocol Spec](references/spec.md)
- [Default Chart of Accounts](references/accounts.md)
- [Verticals](references/verticals.md)
- [biz-in-a-box GitHub project](https://github.com/taylorhou/biz-in-a-box)
- [biz-in-a-box website](https://biz-in-a-box.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify ledger-oriented files such as journal.ndjson, entity.yaml, accounts.yaml, labels.yaml, access.yaml, and vertical specifications.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
