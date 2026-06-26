## Description: <br>
Insert rich Markdown content (including tables) into Feishu documents. Use when feishu_doc write/append fails with tables, or when inserting complex formatted content (tables, code blocks, nested lists) into an existing document at a specific position. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to insert or replace formatted Markdown content in Feishu documents, especially when tables, code blocks, nested lists, or precise insertion positions are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on Feishu documents and may require app scopes that permit document changes. <br>
Mitigation: Verify Feishu app scopes before use and avoid broad workspace permissions. <br>
Risk: Replace or overwrite actions can remove existing document content. <br>
Mitigation: Require explicit user confirmation before replace operations and review the target document token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deadblue22/feishu-md2blocks) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu Markdown block conversion API](https://open.feishu.cn/open-apis/docx/v1/documents/blocks/convert) <br>
- [Feishu document descendant block API](https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{parent_id}/descendant) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Text] <br>
**Output Format:** [Markdown input converted into Feishu document blocks, with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append, insert after a block, or replace document content through Feishu document APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
