## Description:

Helps manage an art-book knowledge base by scanning downloads, archiving new books, syncing with Baidu Netdisk, verifying sync status, and reporting collection statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingxiahotmail](https://clawhub.ai/user/qingxiahotmail)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local art-book library, organize newly downloaded book files into categories, keep a Baidu Netdisk copy synchronized, and inspect collection counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can copy broad local document files into a Baidu-synced folder.

Mitigation: Point config.json only at a dedicated Downloads or staging folder and manually review the file list before running archive_books.py or sync_to_baidu.py.

Risk: Incorrect or overlapping knowledge-base and Baidu paths could copy files to unintended locations.

Mitigation: Verify that the knowledge-base and Baidu paths are distinct, non-overlapping folders before running sync or archive commands.

Risk: The sharing guide discusses redistributing book files.

Mitigation: Share book collections only when the user has the right to redistribute those materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingxiahotmail/skills/art-knowledge-helper)
- [Publisher profile](https://clawhub.ai/user/qingxiahotmail)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and PowerShell commands plus JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file-management guidance and scripts that operate on user-configured knowledge-base, cloud-sync, and downloads paths.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
