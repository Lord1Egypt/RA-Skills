## Description:

Generate professional PDF invoices, payment reminders, and related billing documents with customizable line items, taxes, discounts, currency, and payment details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, small businesses, and agents assisting them use this skill to create local invoice PDFs and payment reminders from command-line inputs, including client details, itemized charges, taxes, discounts, due dates, and payment notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated invoices and reminders can contain client, payment, and bank details.

Mitigation: Use an explicit output path in a private folder and avoid adding unnecessary bank details to PDFs stored in shared or synced directories.

Risk: The skill depends on `fpdf2`, and the artifact suggests installing it without a pinned version.

Mitigation: Install `fpdf2` through a trusted, pinned dependency process before running the invoice script.

Risk: The invoice counter is stored locally under ~/.invoices, which may reveal invoice numbering patterns on shared systems.

Mitigation: Run the skill under an appropriate user account and protect the local home directory when invoices are business-sensitive.

## Reference(s):


## Skill Output:

**Output Type(s):** [PDF files, Shell commands, Guidance]

**Output Format:** [Local PDF documents with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PDFs are written to the selected output path, and invoice numbering state is stored locally under ~/.invoices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
