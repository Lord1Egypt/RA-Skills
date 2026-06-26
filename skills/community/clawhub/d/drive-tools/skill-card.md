## Description: <br>
Drive Tools helps an agent configure and manage SMB, WebDAV, and FTP drives for listing, uploading, downloading, searching, moving, and deleting remote files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SmileTM](https://clawhub.ai/user/SmileTM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect configured personal or team drives over SMB, WebDAV, or FTP, then run guided file management operations from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and uses credentials for configured remote drives. <br>
Mitigation: Use least-privilege drive accounts and keep config.json out of source control and shared workspaces. <br>
Risk: The skill can delete or move remote files. <br>
Mitigation: Manually verify the target drive alias and path before running rm or mv operations. <br>
Risk: FTP TLS mode is called out by the security guidance as unsafe until certificate verification is fixed. <br>
Mitigation: Avoid FTP TLS mode unless certificate verification has been reviewed and corrected. <br>


## Reference(s): <br>
- [Drive Tools on ClawHub](https://clawhub.ai/SmileTM/drive-tools) <br>
- [SMB usage guide](smb_usage_guide.md) <br>
- [WebDAV usage guide](webdav_usage_guide.md) <br>
- [FTP usage guide](ftp_usage_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read, write, move, or delete files on configured remote drives.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
