## Description:

Drive Tools helps agents configure and run SMB, WebDAV, and FTP command-line tools for listing, uploading, downloading, searching, moving, creating, and deleting files on personal drives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smiletm](https://clawhub.ai/user/smiletm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to connect an agent to personal SMB, WebDAV, or FTP drives and perform routine remote file-management tasks. It is best suited for guided drive configuration, connection testing, directory inspection, file transfer, search, move, folder creation, and deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable drive credentials are stored in config.json for SMB, WebDAV, and FTP connections.

Mitigation: Use dedicated low-privilege drive accounts, keep config.json out of version control and backups, and rotate credentials if the file is exposed.

Risk: The scripts support destructive or overwriting remote file operations, including upload, move, download overwrite, and delete.

Mitigation: Manually confirm exact source and destination paths before execution, especially for delete, move, upload, and download commands.

Risk: FTP configurations may use cleartext transport or weak FTPS validation.

Mitigation: Avoid plain FTP where possible and do not rely on this tool as proof of secure FTPS certificate validation.

## Reference(s):

- [Drive Tools ClawHub Page](https://clawhub.ai/smiletm/skills/drive-tools)
- [SMB Usage Guide](artifact/smb_usage_guide.md)
- [WebDAV Usage Guide](artifact/webdav_usage_guide.md)
- [FTP Usage Guide](artifact/ftp_usage_guide.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, text]

**Output Format:** [Markdown with JSON and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute remote drive operations through bundled Python scripts when the user supplies configured connection details.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
