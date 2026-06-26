## Description: <br>
Feishu File Manager helps agents read, download, and process files from Feishu Drive, including PDF, Word, PowerPoint, and Excel documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caspian9](https://clawhub.ai/user/caspian9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to access Feishu Drive links, retrieve tenant tokens, download shared cloud files, validate file or folder access, and parse downloaded office documents for user-facing analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lists broader Feishu permissions than are needed for read and download workflows, including write-capable document scopes. <br>
Mitigation: Use a dedicated Feishu app and grant only the minimum read, metadata, and download scopes required for the intended files. <br>
Risk: Feishu app secrets and tenant access tokens are used to authenticate Drive API requests. <br>
Mitigation: Keep app secrets and tenant tokens out of shared prompts, logs, and artifacts, rotate tokens when exposed, and rely on short token lifetimes. <br>
Risk: Downloaded files may contain sensitive business data and are written to temporary local paths before parsing. <br>
Mitigation: Delete temporary downloads after processing and avoid persisting extracted document contents unless the user explicitly requires it. <br>
Risk: File access can fail when a file or folder has not been shared with the Feishu bot. <br>
Mitigation: Validate file and folder access before processing and report authorization or missing-file errors without retrying with broader permissions by default. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caspian9/feishu-file-manager) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu Drive file download API](https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/download) <br>
- [Feishu Drive file metadata API](https://open.feishu.cn/open-apis/drive/v1/files/{file_token}) <br>
- [Feishu Drive folder listing API](https://open.feishu.cn/open-apis/drive/v1/files?parent_node={folder_token}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with JSON, bash, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe Feishu app credentials, tenant access tokens, file tokens, Drive API calls, local temporary downloads, and document parsing steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
