## Description: <br>
Upload, download, and manage files in Dropbox with automatic OAuth token refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thekie](https://clawhub.ai/user/thekie) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, engineers, and automation users use this skill to let an agent list, search, upload, download, and create Dropbox folders from headless or cross-platform environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Dropbox token file can expose Dropbox app credentials and refresh tokens if committed, shared, or left with broad file permissions. <br>
Mitigation: Keep ~/.config/atlas/dropbox.env private with restrictive permissions such as 600, do not commit or share it, and revoke the Dropbox app if the token file may have been exposed. <br>
Risk: Broad Dropbox app access or mistaken paths can affect more files than intended during upload and download operations. <br>
Mitigation: Prefer an App Folder-scoped Dropbox app over Full Dropbox when possible and review upload and download paths before running commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thekie/dropbox-lite) <br>
- [Dropbox Developers](https://www.dropbox.com/developers) <br>
- [Dropbox OAuth Guide](https://developers.dropbox.com/oauth-guide) <br>
- [Dropbox API Explorer](https://dropbox.github.io/dropbox-api-v2-explorer/) <br>
- [Dropbox API Documentation](https://www.dropbox.com/developers/documentation) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text CLI output, shell commands, configuration values, and Dropbox or local file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Dropbox API credentials stored in ~/.config/atlas/dropbox.env and may update DROPBOX_ACCESS_TOKEN during token refresh.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
