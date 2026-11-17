## Description:

Local-first resource indexing skill for Command Compass that converts user-approved files, folders, links, skill files, downloads folders, website favorites, and prompt resources into CardSchema v1 cards for direct Windows client import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Command Compass users use this skill to turn explicitly approved local resources and website favorites into importable CardSchema v1 cards. It is intended to preserve local-first privacy boundaries by avoiding full-disk scans, unapproved file reads, and public upload of local paths or sensitive identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes website API, account storage, and downloadable ZIP replacement instructions in addition to the local card-generation skill.

Mitigation: Use the artifact only for local card generation unless a separate website maintenance review and approval process authorizes those website changes.

Risk: Cards may refer to local files, folders, executables, shortcuts, scripts, downloads folders, or website favorites.

Mitigation: Generate cards only from user-approved resources, keep shell permission false, and require client confirmation before opening executable-like targets.

Risk: Local paths, file names, file contents, usage history, tokens, cookies, passwords, API keys, or private identifiers could be exposed if privacy boundaries are ignored.

Mitigation: Do not scan the full disk, do not read unapproved file contents, and do not upload local or sensitive data to public market or website sync channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/command-compass-daily-file-index)
- [Publisher profile](https://clawhub.ai/user/addogiavara-tech)
- [Command Compass website](https://www.wboke.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [UTF-8 JSON cards following Command Compass CardSchema v1, with human-readable instructions and optional implementation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated cards use instruction as the copy field, conservative permissions, explicit resourceKind values, and top-level Command Compass client fields.]

## Skill Version(s):

1.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
