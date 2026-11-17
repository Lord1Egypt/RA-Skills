## Description:

Guides agents through sending files to Feishu conversations and creating or updating Feishu cloud documents using the Feishu Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songweisong](https://clawhub.ai/user/songweisong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to send files to Feishu recipients, create Feishu cloud documents, write document content, and troubleshoot common Feishu Bot API request issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may upload the wrong file or disclose sensitive file contents through Feishu.

Mitigation: Review file contents and file paths before upload, and install the skill only when Feishu file or document operations are intended.

Risk: A file or document link may be sent to the wrong Feishu recipient.

Mitigation: Confirm recipient identifiers such as open_id, user_id, union_id, or chat_id before sending messages.

Risk: Feishu app secrets or access tokens may be exposed in shared logs or transcripts.

Mitigation: Store app secrets and access tokens in protected environment variables or a secret manager instead of pasting real credentials into shared text.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu Message Create API](https://open.feishu.cn/document/server-docs/im-v1/message/create)
- [Feishu Document API](https://open.feishu.cn/document/server-docs/docs/docx-v1/document)
- [ClawHub Skill Page](https://clawhub.ai/songweisong/skills/feishu-file-operations)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for third-party Feishu API workflows; agents may produce commands and request payloads for the user to review before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
