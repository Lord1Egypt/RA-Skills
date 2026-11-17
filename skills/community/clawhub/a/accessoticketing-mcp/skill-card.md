## Description:

Read accesso-powered mobile ticket links (accessoticketing.com media-engine URLs from confirmation emails) — order number, per-ticket product, participant, date/time, barcodes, Google Wallet passes — with curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External ticket holders and support staff can use the skill to read order and ticket details from an Accesso mobile-ticket link, including participant names, dates, barcode information, and Google Wallet pass links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ticket URL contains an order token that grants access to tickets and barcodes; parsed output can also contain barcode and personal information.

Mitigation: Treat ticket URLs and results as secrets. Do not paste them into files, commits, or issues, and store any generated barcode images securely.

Risk: ClawScan reports a file-writing weakness and says inspection of the referenced script was incomplete.

Mitigation: Review the reported file-writing issue and confirm the skill’s network access and runtime permissions before installing.

## Reference(s):

- [Ticket parser](artifact/references/parse-tickets.mjs)
- [Ticket parsing recipes](artifact/references/recipes.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands]

**Output Format:** [Structured JSON ticket and order details; optional barcode PNG files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ticket details may include personal information and barcode data; barcode images are optional.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
