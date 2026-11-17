## Description:

Feishu Fetch downloads file, image, and audio attachments from Feishu group messages to local files using configured Feishu app credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch Feishu message attachments for local processing, inspection, conversion, or downstream forwarding workflows. It is intended for received file, image, and audio messages, not for sending messages or reading Feishu Drive, Wiki, Bitable, or cloud documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default download path can be influenced by a remote attachment filename and may overwrite local files.

Mitigation: Use an explicit trusted --output path and avoid running the skill on messages from untrusted senders until attachment filenames are sanitized and unintended overwrites are prevented.

## Reference(s):

- [ClawHub Feishu Fetch skill page](https://clawhub.ai/axelhu/skills/feishu-fetch)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu message endpoint](https://open.feishu.cn/open-apis/im/v1/messages/{message_id})
- [Feishu message resource endpoint](https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{resource_key})

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text stdout path plus a downloaded local attachment file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns process exit codes for success, API errors, parameter errors, missing messages, and permission failures.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
