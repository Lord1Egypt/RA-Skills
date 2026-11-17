## Description:

Read and extract content from all Feishu (Lark) document types using the official Feishu Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfredxia-ai](https://clawhub.ai/user/alfredxia-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to read Feishu/Lark documents, sheets, bitables, and wiki nodes through Feishu Open API credentials, then pass extracted JSON or text content into agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials can be exposed through configuration files or packaged copies.

Mitigation: Store credentials in environment variables or an untracked local config file, restrict file permissions, and remove configured credential files before packaging or sharing the skill.

Risk: Retrieved Feishu content may be sensitive and can be printed into the agent session or logs.

Mitigation: Use the smallest Feishu permissions and document scope needed, avoid recursive wiki reads unless necessary, and handle outputs as sensitive data.

Risk: Command-execution integration examples can become unsafe if untrusted input is interpolated into shell commands.

Mitigation: Validate document tokens and URLs, pass arguments without shell interpolation where possible, and review command construction before using agent-provided input.

## Reference(s):

- [Feishu Open API Documentation](https://open.feishu.cn/document)
- [Authentication Guide](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token_internal)
- [Document API (docx)](https://open.feishu.cn/document/server-docs/docs/docx-v1/document)
- [Document Blocks API](https://open.feishu.cn/document/server-docs/docs/docx-v1/document-block)
- [Sheet API Reference](https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet/get)
- [Bitable API Reference](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app/get)
- [Bitable Records API](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-record/list)
- [Wiki API Overview](https://open.feishu.cn/document/server-docs/docs/wiki-v2/wiki-overview)
- [Wiki Node API](https://open.feishu.cn/document/server-docs/docs/wiki-v2/space-node/list)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON or plain text content, with Markdown guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and document, sheet, bitable, or wiki tokens; recursive wiki reads can expand retrieved content.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
