## Description:

Generates professional PDF invoices from structured JSON input using jsPDF, with configurable branding, EUR/GBP/USD support, multi-item tables, and payment details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexwong27](https://clawhub.ai/user/alexwong27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business users use this skill to generate invoice PDFs from structured invoice JSON and reusable company configuration in constrained Node.js environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated invoices and configuration can contain customer, billing, IBAN, and SWIFT details written to disk.

Mitigation: Use a private secured outputDir, protect configuration files, avoid shared temp locations for real invoices, and delete generated PDFs when no longer needed.

Risk: The local Node script reads invoice JSON and configuration files and writes a PDF to the filesystem.

Mitigation: Run it only with trusted local invoice data and review the chosen input and output paths before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexwong27/skills/clawed-invoice)
- [Configuration Reference](artifact/references/config.json)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration]

**Output Format:** [PDF file plus a text path printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes invoice-<invoiceNumber>.pdf to the configured outputDir, defaulting to /tmp/invoices.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
