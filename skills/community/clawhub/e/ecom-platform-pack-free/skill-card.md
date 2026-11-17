## Description:

把电商与平台结算材料按 14 项检查逐客户核对，每个客户输出一行结论，并为发现项提供原文文件与行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, operations teams, and finance staff use this skill before settlement cycles to check e-commerce, platform, mall, franchise, OTA, live-commerce, rebate, points, subsidy, consignment, and restaurant daily-sales materials by client. It helps identify arithmetic, reconciliation, coverage, and source-line issues without replacing audit, legal, or accounting certification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local settlement materials may contain sensitive commercial or financial data.

Mitigation: Run the skill only on files you intend to expose to the local agent workspace, and avoid sharing generated outputs beyond the reviewers who need them.

Risk: The findings are reconciliation assistance, not audit, legal, accounting, or payment certification.

Mitigation: Have qualified staff verify material findings against the cited source files and line references before making settlement or escalation decisions.

Risk: The free edition explicitly omits advanced cross-client summary, risk-ranking, categorization, and ledger export capabilities.

Mitigation: Review the listed non-run checks and use separate review steps or another edition when cross-client reporting or exports are required.

Risk: Missing or poorly structured input can cause checks to be unexecuted rather than passed.

Mitigation: Use one client per directory, provide the required settlement materials, preserve clear table sections, and treat any unexecuted item as not reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ecom-platform-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is plain text or JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local settlement files selected by the user and prints findings with source file and line references; no files are written by the skill.]

## Skill Version(s):

1.0.29 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
