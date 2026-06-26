## Description: <br>
DingTalk Cloud Storage Assistant helps agents manage DingTalk Drive team spaces, files, uploads, downloads, and DingTalk document read/write workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andylikescodes](https://clawhub.ai/user/andylikescodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise administrators use this skill to guide agents through DingTalk Drive storage operations, including listing spaces and files, configuring permissions, uploading or downloading files, and reading or writing DingTalk documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable DingTalk operations can overwrite or alter enterprise documents. <br>
Mitigation: Use least-privilege DingTalk credentials, restrict writes to approved folders, confirm target documents before write operations, and keep backups before using overwrite workflows. <br>
Risk: DingTalk AppKey and AppSecret provide API access to enterprise resources. <br>
Mitigation: Provide credentials only through environment variables or a secret manager, avoid storing them in skill files or prompts, and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [Permissions Guide](PERMISSION_GUIDE.md) <br>
- [DingTalk Permission Setup](references/permissions.md) <br>
- [Permission List for Administrators](references/permission-list-share.md) <br>
- [Upload Guide](references/upload-guide.md) <br>
- [DingTalk Open Platform Permission Management](https://open.dingtalk.com/document/orgapp-server/permission-management) <br>
- [DingTalk Drive API Documentation](https://open.dingtalk.com/document/development/knowledge-base-download-file) <br>
- [DingTalk Document API](https://open.dingtalk.com/document/development/dingtalk-document-model) <br>
- [DingTalk Internal App Access Token](https://open.dingtalk.com/document/orgapp-server/obtain-the-access_token-of-an-internal-app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk OAuth credentials from environment variables and DingTalk app permissions for requested operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
