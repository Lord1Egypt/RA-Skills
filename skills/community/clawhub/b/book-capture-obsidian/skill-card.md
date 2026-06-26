## Description: <br>
Capture and normalize book metadata into Obsidian Markdown notes from photos or Goodreads CSV exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ricardodpalmeida](https://clawhub.ai/user/Ricardodpalmeida) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to import book photos or Goodreads CSV exports into an Obsidian vault as normalized, idempotent Markdown notes and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk migration or note upsert can change an Obsidian vault. <br>
Mitigation: Back up or version-control the vault and run migrations with dry-run before live writes. <br>
Risk: Default Goodreads enrichment may send library metadata to Google Books. <br>
Mitigation: Disable Google enrichment for sensitive libraries, or use a restricted Google Books API key. <br>
Risk: Bundled CI or pytest checks may import Python files from an overly broad parent directory. <br>
Mitigation: Run checks only in a clean sandbox or after constraining tests to import the intended skill modules. <br>


## Reference(s): <br>
- [Book Capture Obsidian Skill Page](https://clawhub.ai/Ricardodpalmeida/book-capture-obsidian) <br>
- [Configuration](references/configuration.md) <br>
- [Data Contracts](references/data-contracts.md) <br>
- [Migration Runbook](references/migration-runbook.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes, JSON envelopes, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deterministic Obsidian note updates and dashboard content when run against a configured vault.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
