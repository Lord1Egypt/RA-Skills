## Description:

A Feishu document management skill for creating, reading, writing, deleting, and clearing Feishu documents and document blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkingmanyangyang](https://clawhub.ai/user/thinkingmanyangyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Feishu documents through PowerShell examples and Feishu Open Platform APIs, including document creation, content reads and writes, block deletion, full document replacement, and Wiki document token handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Feishu document authority, including collaborator-management permissions.

Mitigation: Grant only the Feishu scopes needed for the intended operations and avoid docs:permission.member unless collaborator management is required.

Risk: The skill includes examples that delete blocks or clear document content.

Mitigation: Require explicit confirmation and verify the target document and block range before any delete or clear-document action.

Risk: The weather update example inserts external content into JSON by string concatenation.

Mitigation: Treat that example as unsafe sample code unless rewritten to serialize JSON safely and limit external content.

## Reference(s):

- [Feishu Docx Document API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document)
- [Feishu Batch Delete Blocks API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/children/batch_delete)

## Skill Output:

**Output Type(s):** [shell commands, code, configuration, guidance]

**Output Format:** [Markdown with PowerShell code blocks and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for Feishu API calls, token setup, document block operations, and common Feishu error handling.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
