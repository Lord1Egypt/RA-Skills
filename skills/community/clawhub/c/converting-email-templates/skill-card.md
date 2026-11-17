## Description:

Converts or migrates email templates from SendGrid, Mailgun, Mandrill, Postmark, Brevo, and Amazon SES to Mailtrap-compatible Handlebars syntax for single files, directories, or inline HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert existing provider-specific email template syntax into Mailtrap-compatible Handlebars and to identify application-side changes needed after migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter can overwrite source or existing files when the output path overlaps important files.

Mitigation: Run conversions on copies or backups, choose a dedicated empty output directory, and avoid pointing output at the source folder.

Risk: Mailtrap API examples include update and delete operations that can change or remove templates.

Mitigation: Treat curl snippets as manual examples, use appropriately scoped tokens, and review identifiers before running update or delete requests.

## Reference(s):

- [Template Conversion Rules](references/conversion-rules.md)
- [How to Migrate Email Templates to Mailtrap](content/how-to-migrate-email-templates.md)
- [Mailtrap Email Templates documentation](https://docs.mailtrap.io/email-api-smtp/email-templates)
- [Mailtrap sending domain setup](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain.md)
- [Mailtrap authentication documentation](https://docs.mailtrap.io/developers/authentication)
- [ClawHub skill page](https://clawhub.ai/mailtrap/skills/converting-email-templates)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and Handlebars code blocks; converted HTML files and text reports when file conversion is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce converted template files, per-file report files, and a bulk summary file in the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
