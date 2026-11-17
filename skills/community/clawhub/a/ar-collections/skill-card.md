## Description:

AR Collections helps agents run an accounts-receivable aging and collections analysis workflow for QBO clients, producing a seven-tab Excel workbook with aging buckets, DSO, collection priorities, bad debt reserve, payment patterns, and CDC changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, and controller teams use this skill to create QBO accounts-receivable aging, collections priority, DSO, payment pattern, bad debt reserve, and month-end AR review outputs. It is intended for AR-focused reporting and should not be used for bank reconciliation, payroll, tax preparation, P&L, or balance sheet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses QBO accounts-receivable data and writes generated workbook and cache files that may contain sensitive financial or customer information.

Mitigation: Confirm the client slug and output directory before running, and apply cleanup or retention controls to the workbook and .cache/ar-collections/{slug}.json.

Risk: Running the workflow for an inapplicable client could produce unnecessary or misleading AR output.

Mitigation: Confirm AR applicability against the client SOP and rely on the documented auto-skip behavior for clients with no accounts receivable.

Risk: Runtime dependency or QBO authentication issues can affect report generation.

Mitigation: Use a dedicated non-root virtual environment, pin openpyxl where possible, and verify QBO client access before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/skills/ar-collections)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash command examples and an Excel workbook file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a seven-tab AR collections workbook and a local CDC cache for comparing customer balance and aging-bucket movement between runs.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
