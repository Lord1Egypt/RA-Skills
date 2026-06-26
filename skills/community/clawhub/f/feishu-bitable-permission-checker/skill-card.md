## Description: <br>
飞书多维表格文档权限检查工具：根据用户提供的飞书多维表格 URL 或 app_token，提取「链接地址」列并批量检查 docx/wiki 文档的阅读权限。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganguagua](https://clawhub.ai/user/ganguagua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or workspace administrators use this skill to check which Feishu documents listed in a Bitable are readable by the active Feishu account. It produces a concise permission report split into readable and unreadable document lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Permission reports can expose employee names, document links, document titles, and access outcomes. <br>
Mitigation: Run the check only in an appropriate private context and share results only with the owner or authorized reviewers. <br>
Risk: Using the wrong Feishu account can produce misleading permission results. <br>
Mitigation: Run the skill with the Feishu account whose access should be tested and confirm the Bitable and linked documents are appropriate for a batch check. <br>
Risk: Feishu rate limits or transient network errors can cause incorrect no-permission classifications if treated as final failures. <br>
Mitigation: Use the documented bounded concurrency and retry behavior before marking a document as inaccessible. <br>


## Reference(s): <br>
- [Feishu API Notes for Bitable Permission Checker](references/api_notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/ganguagua/feishu-bitable-permission-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown permission report with tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates documents with and without read permission and includes employee names, document titles when available, and document links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
