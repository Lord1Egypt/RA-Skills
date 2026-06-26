## Description: <br>
Read and extract content from Feishu and Lark documents using the official Feishu Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlfredXia-AI](https://clawhub.ai/user/AlfredXia-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to retrieve Feishu or Lark documents, spreadsheets, bitables, and wiki content for downstream analysis, summarization, or workflow automation. It supports both structured JSON output and simplified text extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials can grant read-only access to documents and spaces shared with the app. <br>
Mitigation: Use a dedicated low-privilege Feishu app, share only approved documents or spaces, and protect credentials with file permissions or environment variables. <br>
Risk: Wiki-space and recursive modes can bring large amounts of workspace content into the agent session. <br>
Mitigation: Use recursive reads only when intended, scope access to approved spaces, and prefer targeted document tokens or simplified output for large content. <br>
Risk: Retrieved documents may contain sensitive business or personal information. <br>
Mitigation: Review document access before execution and handle extracted text or JSON according to the organization's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlfredXia-AI/feishu-document-reader) <br>
- [Feishu Open API Documentation](https://open.feishu.cn/document) <br>
- [Feishu Authentication Guide](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token_internal) <br>
- [Document Blocks API](https://open.feishu.cn/document/server-docs/docs/docx-v1/document-block) <br>
- [Sheet API Reference](https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet/get) <br>
- [Bitable API Reference](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or plain text from shell and Python commands, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, Feishu app credentials, and document or space access; output size depends on the selected document, wiki space, and recursive options.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
