## Description:

Manage freelance clients, projects, invoices, communications, deadlines, and freelance business operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanwyngaard](https://clawhub.ai/user/seanwyngaard)

### License/Terms of Use:


## Use Case:

Freelancers and small-service operators use this skill to maintain client and project records, track time and deliverables, generate invoices, prepare client updates, and review business status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell access that is not necessary for the documented freelance-management workflow.

Mitigation: Review before installing and remove Bash from allowed tools unless a deployment-specific need is identified.

Risk: Client, invoice, payment, and project details are stored as ordinary local files.

Mitigation: Use only in a private, access-controlled workspace, keep freelance-data/ out of git and shared sync locations, and avoid storing bank account numbers, routing numbers, credentials, or tokens.

Risk: Generated invoices, payment reminders, and client updates may contain errors or inappropriate wording.

Mitigation: Review generated invoices and communications before sending them to clients.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, html, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON files, and plain-text dashboard or email content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under freelance-data/, including client records, project records, time logs, invoices, updates, and configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
