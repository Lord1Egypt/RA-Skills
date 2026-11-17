## Description:

Generate and upload FBA customs invoices for CATCH, the Amazon SEND partnered carrier, and similar forwarder portals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-school](https://clawhub.ai/user/claw-school)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and logistics operators use this skill to turn FBA inbound-plan data and product master data into CATCH-compatible customs invoice files, then upload approved invoices to the forwarder to place orders.

### Deployment Geography for Use:

China and United States freight workflows

## Known Risks and Mitigations:

Risk: The skill handles CATCH portal credentials, cached tokens, and arbitrary portal URLs.

Mitigation: Use a verified HTTPS CATCH portal URL, pass credentials through the environment only, avoid broad ERP or database credentials, and run in a constrained project environment.

Risk: Uploading generated invoices places or updates forwarder orders.

Mitigation: Review each generated invoice before upload and require explicit user approval before running upload commands.

Risk: Incorrect HS codes, declared values, battery flags, or magnet flags can create customs or safety declaration problems.

Mitigation: Use the user's system of record for product data and have the user or customs broker confirm declaration values before upload.

Risk: Forwarder template changes can shift invoice fields and cause rejected or incorrect declarations.

Mitigation: Run the template drift check after template updates, regenerate one invoice, and test a single upload before batch generation.

## Reference(s):

- [Data schemas](reference/data-schemas.md)
- [ClawHub skill page](https://clawhub.ai/claw-school/skills/amazon-send-catch-invoice)
- [Claw School](https://claw-school.com)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, BMP, and XLS files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated invoices are written as .xls records; upload commands can place or update CATCH forwarder orders.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
