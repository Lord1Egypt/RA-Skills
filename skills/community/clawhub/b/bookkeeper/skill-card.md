## Description:

Automates invoice intake from Gmail, extracts invoice data with OCR, verifies payment in Stripe, and creates reconciliation-ready accounting entries in Xero.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

External users and finance operations teams use this skill to process invoice emails into structured bookkeeping records, verify payment evidence, and prepare Xero accounting entries with manual-review safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and update instructions use mutable unpinned packages and an unrestricted bulk update command in a finance and email automation context.

Mitigation: Review install steps before use, prefer pinned and reviewed versions of clawhub and the required skills, and avoid update --all where production Gmail, Stripe, OCR, or Xero credentials are available.

Risk: The skill uses credentials that can access email, payment, OCR, and accounting systems.

Mitigation: Use least-privilege accounts, verify required environment variables before execution, and keep auto-posting on manual review unless configured accounting controls are acceptable.

Risk: Uncertain OCR fields, ambiguous payment matches, or missing payment evidence could lead to incorrect accounting status.

Mitigation: Route records with critical hil_flag values, ambiguous matches, or failed quality gates to ReviewQueue, and never mark an invoice as paid without payment evidence.

Risk: Accounting writes may create duplicate or unintended records if prior entries are not checked.

Mitigation: Use vendor, invoice number, total, source message ID, and idempotency keys for duplicate checks; never silently overwrite existing accounting records.

## Reference(s):

- [Bookkeeper ClawHub Skill Page](https://clawhub.ai/h4gen/skills/bookkeeper)
- [Publisher Profile](https://clawhub.ai/user/h4gen)
- [Inspected Upstream Skills](artifact/references/inspected-skills.md)
- [ClawHub Homepage](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown with structured bookkeeping summaries and optional JSON transaction records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns IntakeSummary, ExtractionSummary, PaymentVerification, AccountingAction, and ReviewQueue sections; may include created or updated record IDs and manual-review status.]

## Skill Version(s):

1.0.0 (source: evidence.release.version; changelogSource: user)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
