## Description:

Indexes EML emails into an SQLite database, providing a web interface for searching, management, Excel export, and file deletion, with IP access control and integrated JSON automated backup/restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamfromtw](https://clawhub.ai/user/williamfromtw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and records teams can use this skill to index local EML archives into SQLite, search messages through a local web interface, export results, and manage JSON backup and restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive email contents, file paths, exported CSV data, and JSON backup archives.

Mitigation: Run it only in a controlled local environment, restrict access to trusted hosts, and protect the generated database, exports, and backups as sensitive data.

Risk: The default admin password and weak admin controls could expose management actions if the Flask server is reachable by untrusted clients.

Mitigation: Change the admin password before use and avoid exposing the server outside trusted local networks.

Risk: Restored backups and indexed email content are untrusted inputs that may carry unsafe content.

Mitigation: Treat all EML files and uploaded backup ZIPs as untrusted, and review or patch restore validation and XSS handling before use on important archives.

Risk: Admin file deletion and backup retention behavior can remove files from disk.

Mitigation: Review path-containment checks, test deletion on copies, and keep independent backups before enabling deletion on production mail archives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamfromtw/skills/eml-to-sqlite-indexer)
- [Traditional Chinese skill documentation](references/SKILL-TW.md)
- [Bootstrap documentation](https://getbootstrap.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration details, and file-oriented workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for creating an SQLite email index, running a local Flask interface, exporting CSV data, and managing JSON ZIP backups.]

## Skill Version(s):

7.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
