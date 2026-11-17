## Description:

Sync and manage CardDAV contacts (Google, iCloud, Nextcloud, etc.) using vdirsyncer + khard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcromero](https://clawhub.ai/user/jcromero)

### License/Terms of Use:


## Use Case:

Developers, operators, and power users use this skill to configure vdirsyncer and khard for CardDAV contact synchronization, lookup, editing, and address-book management from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CardDAV synchronization can delete or overwrite contacts when conflicts or address-book mappings are misconfigured.

Mitigation: Review vdirsyncer collections and conflict_resolution settings before first sync, keep a contact backup, and run an initial sync against a test or known-safe address book when possible.

Risk: The example password.fetch command reads an app-password file from disk, which can expose credentials if file permissions are loose.

Mitigation: Store app-password files with strict user-only permissions or use a keyring-backed command instead of a broadly readable file.

Risk: khard remove and move commands can affect the wrong contact when a search term matches multiple records.

Mitigation: Show or list matching contacts first and confirm the exact contact before running delete or move commands.

## Reference(s):

- [ClawHub CardDAV Contacts release page](https://clawhub.ai/jcromero/skills/carddav-contacts)
- [Google CardDAV well-known endpoint](https://www.googleapis.com/.well-known/carddav)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and INI configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes Linux with vdirsyncer and khard installed.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
