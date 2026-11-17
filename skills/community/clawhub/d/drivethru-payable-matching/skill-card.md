## Description:

Reconciles vendor payable documents and Sports Inc invoices against Odoo purchase orders, corrects supported PO price variances, routes unresolved items for review, and creates or posts vendor bills only when totals match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and purchasing operators use this skill to reconcile vendor confirmations, acknowledgements, and invoices against Odoo purchase orders, update clearly supported price variances, file reviewed documents, and prepare or post matched payables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Odoo purchasing and accounting records, including PO pricing and vendor bill state.

Mitigation: Install only where that authority is intended, use least-privilege Odoo/MCP credentials, and require human authorization for bill posting, quantity changes, dropship validation, and credential-sharing delegation.

Risk: A mismatched payable could be posted if totals or invoice structure are not checked.

Mitigation: Prefer draft or dry-run operation until the workflow is proven, leave mismatches in draft, and post only when the bill total matches the source invoice within tolerance.

Risk: Runtime dependency bootstrapping can install Python packages into a cached environment.

Mitigation: Review the dependency bootstrapping policy and preinstall or approve the declared packages before production use.

## Reference(s):

- [Payable matching procedure](references/matching_procedure.md)
- [Sports Inc payables procedure](references/sportsinc_payables.md)
- [Odoo](https://www.odoo.com)
- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/drivethru-payable-matching)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command payloads and concise reconciliation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run Odoo MCP operations through native tools or scripts/paymatch.py; helper commands return JSON objects.]

## Skill Version(s):

0.10.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
