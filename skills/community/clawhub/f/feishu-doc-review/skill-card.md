## Description:

Feishu Doc Review helps an agent add highlights, underlines, and document-level comments to Feishu cloud documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipng05-max](https://clawhub.ai/user/yipng05-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review and revise Feishu documents by applying block-level highlights or underlines and by adding document-level comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make credential-backed changes to Feishu documents.

Mitigation: Require explicit user confirmation before each document-changing action and narrow activation to explicit Feishu document URLs or requests.

Risk: The release includes an exposed Feishu app secret.

Mitigation: Remove and rotate the exposed secret and require credentials from a protected runtime source.

Risk: Comment content is passed into a JSON request body by a shell script.

Mitigation: JSON-encode comment content before sending it to the Feishu API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yipng05-max/skills/feishu-doc-review)
- [Feishu Drive comments API endpoint](https://open.feishu.cn/open-apis/drive/v1/files/{doc_token}/comments?file_type=docx)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command invocations and API action names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform credential-backed changes to Feishu documents when invoked with document tokens and comment text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
