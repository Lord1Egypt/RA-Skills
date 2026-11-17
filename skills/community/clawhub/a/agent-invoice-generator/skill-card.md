## Description:

Generates invoice files and status summaries from structured inputs, with PDF output when ReportLab is available and HTML fallback otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to create invoice records, generate invoice documents, and track paid or unpaid invoice status from agent-provided billing details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive invoices and business details.

Mitigation: Use it only in a controlled workspace and review invoice content before sharing generated files.

Risk: File writes are under-scoped and use fixed paths in the user's home directory.

Mitigation: Run with an isolated home directory or inspect ~/.openclaw and ~/Documents/Invoices outputs before relying on them.

Risk: Fallback HTML output may include untrusted client, item, or notes text without sufficient escaping.

Mitigation: Avoid untrusted billing text until HTML escaping is fixed, and prefer reviewed PDF output when available.

Risk: Some advertised recurring, receipt, and view capabilities are not fully implemented.

Mitigation: Do not rely on those features without additional implementation review and approval controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/agent-invoice-generator)
- [Publisher profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [PDF or HTML invoice files, JSON invoice records, and Markdown-style command summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes configuration and invoice data under ~/.openclaw and invoice documents under ~/Documents/Invoices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
