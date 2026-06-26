## Description: <br>
Feishu (Lark) Document API writing spec. Converts Markdown content to Feishu Block structures and writes to cloud docs. Handles concurrency ordering. Use when syncing articles, creating document blocks, or writing long-form content to Feishu docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyyao2222-eng](https://clawhub.ai/user/sunnyyao2222-eng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create or update Feishu/Lark cloud documents from Markdown-like content, including headings, lists, code blocks, callouts, images, tables, and other Docx API block structures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials could be exposed or granted broader document access than needed. <br>
Mitigation: Store app_id and app_secret in environment variables or a secret manager, and grant only the minimum Feishu document scopes required. <br>
Risk: An agent could write content to the wrong Feishu document or folder. <br>
Mitigation: Review document and folder targets before allowing write operations. <br>
Risk: Concurrent block creation can reorder document content. <br>
Mitigation: Use a single batch request when possible, or perform serial writes with explicit indexes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyyao2222-eng/feishu-doc-write) <br>
- [Feishu Create Blocks API](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/document-docx/docx-v1/document-block-children/create) <br>
- [Feishu Block Data Structure](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/document-docx/docx-v1/data-structure/block) <br>
- [Feishu Markdown Convert API](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/document-docx/docx-v1/document/convert) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu Docx block schemas, API endpoints, batching guidance, and credential handling notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
