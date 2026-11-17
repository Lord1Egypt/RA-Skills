## Description:

Save, organize, and search web bookmarks with tags and categories. Use when collecting research links, organizing lists, or reviewing resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep local bookmark, planning, reminder, project, and review notes searchable from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bookmark, plan, reminder, review, and similar entries are stored as plaintext local files.

Mitigation: Do not store secrets or highly sensitive personal data; periodically review or delete local data under ~/.local/share/bookmark-keeper.

Risk: CSV exports may be opened by spreadsheet software without safe value encoding.

Mitigation: Treat exported CSV files as untrusted data, prefer JSON or TXT exports when possible, and sanitize CSV values before opening them in spreadsheets.

Risk: Broad productivity logging can accumulate personal or sensitive context over time.

Mitigation: Limit use to non-sensitive bookmarks and work notes, and review exported content before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/bookmark-keeper)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Plain text CLI output plus plaintext log files and JSON, CSV, or TXT exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local entries under ~/.local/share/bookmark-keeper and can export accumulated entries.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
