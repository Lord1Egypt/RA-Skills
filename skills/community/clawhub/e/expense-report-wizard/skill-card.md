## Description:

Expense Report Wizard helps agents organize China mainland business travel reimbursement materials by extracting invoice data, categorizing expenses, rebuilding itineraries, generating reimbursement reports, and running policy-based compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheyuy](https://clawhub.ai/user/sheyuy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to turn invoice photos, local invoice folders, or text lists into organized travel reimbursement materials, itinerary logs, reimbursement forms, and preliminary compliance findings. Finance and operations reviewers can use the outputs as a structured draft, while final approval, tax treatment, and invoice authenticity checks remain outside the skill.

### Deployment Geography for Use:

Global use for workflows involving China mainland invoice formats

## Known Risks and Mitigations:

Risk: The security evidence says the skill may process sensitive reimbursement data through connected external services without clear per-action consent.

Mitigation: Prefer local-only processing unless the user intentionally approves OCR uploads, online document export, meeting lookup, or notifications.

Risk: Folder and archive processing can expose unrelated files if the selected directory contains more than the intended reimbursement documents.

Mitigation: Use a dedicated folder containing only the invoices for the reimbursement and review archive contents before processing.

Risk: Tencent Cloud secrets or other service credentials could be exposed through chat, logs, screenshots, or shell history.

Mitigation: Keep credentials out of chat and shared logs, and use environment handling that avoids displaying secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheyuy/skills/expense-report-wizard)
- [Source repository from server-resolved provenance](https://github.com/Sheyuy/expense-report-wizard)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables, structured text, CSV-ready exports, and inline shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include invoice classifications, itinerary logs, reimbursement forms, compliance summaries, file-renaming previews, and optional online document export guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter: 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
