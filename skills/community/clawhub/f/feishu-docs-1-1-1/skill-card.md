## Description: <br>
Provides Feishu Docx document operations for creating, reading, updating, deleting, sharing, searching, listing, and converting Markdown or HTML content through Feishu Open Platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binbin](https://clawhub.ai/user/binbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage Feishu Docx documents from an agent workflow, including CRUD operations, content conversion, export, search, folder listing, and permission management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite or delete live Feishu documents without built-in confirmation safeguards. <br>
Mitigation: Use a dedicated least-privilege Feishu app, verify document IDs before update or delete commands, and back up important documents before replacement or deletion. <br>
Risk: Sharing commands can grant document access to the wrong recipient or with excessive permissions. <br>
Mitigation: Verify recipient user IDs and requested permission levels before running share commands. <br>
Risk: Feishu app credentials can authorize read and write access to business documents. <br>
Mitigation: Keep FEISHU_APP_SECRET out of logs and source control, scope app permissions narrowly, and rotate credentials according to organization policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binbin/feishu-docs-1-1-1) <br>
- [Publisher profile](https://clawhub.ai/user/binbin) <br>
- [Feishu Open Platform Docx API documentation](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/overview) <br>
- [Feishu Open Platform app console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript examples; CLI commands may emit JSON, Markdown, or plain text depending on options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET. Commands may make live Feishu API changes, including document replacement, deletion, and sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json and _meta.json list 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
