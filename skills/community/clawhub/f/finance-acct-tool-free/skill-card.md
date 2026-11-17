## Description:

财务会计入门工具 helps individuals and small businesses record transactions, reconcile bank statements, calculate basic taxes, and generate basic financial reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, independent developers, and small business operators use this skill to get agent guidance and command examples for local bookkeeping, reconciliation, basic tax calculation, and financial report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for read and exec authority for financial workflows.

Mitigation: Review commands before execution and limit them to intended local accounting files and trusted working directories.

Risk: The referenced finance.py implementation and runtime setup are not fully established by the evidence.

Mitigation: Confirm the source and behavior of finance.py before using the skill with bank statements, tax data, or production accounting records.

Risk: The local-only privacy claim is under-scoped while network and API behavior are not fully documented.

Mitigation: Use test data first and avoid sensitive financial data until network behavior and data handling are verified.

Risk: Generated bookkeeping, tax, and report guidance may be incomplete or incorrect for a user's jurisdiction or accounting policy.

Mitigation: Have financial and tax outputs reviewed by a qualified person before relying on them for filing, audit, or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/finance-acct-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples, YAML snippets, and report-generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local finance command examples and generated report filenames; actual execution depends on the user's local finance.py implementation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
