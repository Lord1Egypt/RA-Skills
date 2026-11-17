## Description:

DingTalk Cloud Storage Assistant helps agents manage DingTalk Drive spaces, files, uploads, downloads, DingTalk documents, and related collaboration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andylikescodes](https://clawhub.ai/user/andylikescodes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and employees use this skill to guide DingTalk cloud storage operations, including listing spaces and files, reading and writing DingTalk documents, uploading or downloading files, and preparing required app permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad enterprise file reads and DingTalk Drive writes.

Mitigation: Use a dedicated DingTalk app with only the minimum storage scopes required, and restrict write operations to disposable or explicitly approved folders.

Risk: The artifact includes document-write and overwrite examples that could replace existing content.

Mitigation: Require confirmation before overwrite operations and prefer auto-rename or append workflows unless replacement is explicitly intended.

Risk: Credential and token examples can expose secrets if copied into logs or shared files.

Mitigation: Store AppKey and AppSecret in environment variables or secret storage, and remove token-printing commands before operational use.

Risk: Optional contact-directory permissions expand access beyond storage operations.

Mitigation: Do not approve contact-directory permissions unless the deployment explicitly requires user or department lookup.

## Reference(s):

- [Permission Guide](PERMISSION_GUIDE.md)
- [Permissions](references/permissions.md)
- [Permission List Share](references/permission-list-share.md)
- [Upload Guide](references/upload-guide.md)
- [DingTalk Permission Management](https://open.dingtalk.com/document/orgapp-server/permission-management)
- [DingTalk Drive API Documentation](https://open.dingtalk.com/document/development/knowledge-base-download-file)
- [DingTalk Document API](https://open.dingtalk.com/document/development/dingtalk-document-model)
- [DingTalk Internal App Access Token](https://open.dingtalk.com/document/orgapp-server/obtain-the-access_token-of-an-internal-app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DINGTALK_APP_KEY and DINGTALK_APP_SECRET environment variables and DingTalk app permissions.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
