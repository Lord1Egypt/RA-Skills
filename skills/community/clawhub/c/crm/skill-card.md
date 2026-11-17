## Description:

Runs a CRM for contacts, companies, deals, pipeline stages, follow-ups, data hygiene, imports, migrations, forecasting, and deletion or do-not-contact requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to set up, rescue, and operate a CRM for sales, fundraising, donor, job-search, freelance, or relationship pipelines. It helps maintain local records, review deals and follow-ups, clean or import data, choose tools, and handle suppression or deletion requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain durable CRM and contact records containing personal or commercial relationship data.

Mitigation: Review configured data paths before use, minimize stored fields and notes, and keep records within the declared local Clawic data folders.

Risk: Bulk imports, merges, edits, migrations, or deletions can affect many records at once.

Mitigation: Require explicit confirmation for bulk changes and write a dated export or backup before the operation.

Risk: CRM integrations may require API tokens, BCC logging addresses, signed URLs, or other credentials.

Mitigation: Store only credential pointers such as environment, keychain, or password-manager references, and strip pasted secret values before writing notes.

Risk: A contact suggestion, import, or outreach list could include someone who opted out or requested deletion.

Mitigation: Read the do-not-contact list before naming contacts for outreach and preserve suppression entries even when the underlying contact record is removed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/crm)
- [Clawic CRM Skill Page](https://clawic.com/skills/crm)
- [CRM Skill Definition](artifact/SKILL.md)
- [Privacy Procedures](artifact/privacy.md)
- [Import and Migration Procedures](artifact/import.md)
- [Working File Templates](artifact/memory-template.md)
- [CRM Tool Selection](artifact/tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, tables, local file updates, configuration values, and occasional SQL or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local CRM and shared contact notes under configured Clawic data paths, or produce exact rows and changes for a user to apply in an external CRM.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
