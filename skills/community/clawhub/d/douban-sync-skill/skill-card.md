## Description:

Export and sync Douban book, movie, music, and game collections to local CSV files for local management and Obsidian-compatible workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosformula](https://clawhub.ai/user/cosformula)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to export their Douban reading, watching, listening, and gaming history into local CSV files and keep those files updated through RSS-based sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV files may include untrusted external Douban text that spreadsheet software could evaluate.

Mitigation: Open or import generated CSV files with formula evaluation disabled, or inspect and sanitize values before using them in spreadsheet software.

Risk: Full export and recurring sync can write personal Douban activity data to local files.

Mitigation: Use a browser session you control, choose the output directory deliberately, and add recurring sync only when ongoing local collection updates are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosformula/skills/douban-sync-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts generate local CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DOUBAN_USER; CSV outputs may contain untrusted external text from Douban.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
