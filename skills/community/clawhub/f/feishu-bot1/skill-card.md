## Description: <br>
Feishu Bot helps agents create, read, update, and delete Feishu/Lark documents, edit document blocks or table cells, send messages to users or chats, retrieve chat messages, and upload files through Feishu APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellostar999](https://clawhub.ai/user/hellostar999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to automate Feishu/Lark document maintenance, targeted block updates, chat lookup, message delivery, and file sharing from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled test and demo scripts can target fixed Feishu chats or documents and perform live writes without a fresh user-selected destination. <br>
Mitigation: Remove or disable extra test/demo scripts before installation, and require explicit confirmation of every chat ID, document token, and outbound message before execution. <br>
Risk: Some scripts scan local Desktop files or upload inferred spreadsheet files, which can expose unintended local data. <br>
Mitigation: Use only explicit file paths supplied by the operator, review files before upload, and remove scripts that infer local Desktop files by name or size. <br>
Risk: Feishu credentials can grant broad document, messaging, and file permissions if reused or over-scoped. <br>
Mitigation: Use fresh Feishu app credentials with minimal scopes, keep secrets outside shared artifacts, and rotate credentials if they may have been exposed. <br>


## Reference(s): <br>
- [Feishu API Reference](artifact/references/api_ref.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hellostar999/feishu-bot1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live Feishu document, messaging, and file-upload operations when executed with configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
