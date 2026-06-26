## Description: <br>
Feishu Skills is a Feishu and Lark integration skill pack for OpenClaw and EnClaws that lets agents set up a Feishu bot and manage documents, chats, calendars, tasks, bitables, drive files, OCR, sheets, wiki content, and user lookup through per-user OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hashstacs-hk](https://clawhub.ai/user/hashstacs-hk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill pack to connect an agent to Feishu or Lark workspaces, then read, create, update, search, export, and manage workspace content and collaboration objects through authenticated user-scoped actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill pack can grant broad Feishu workspace access through OAuth scopes. <br>
Mitigation: Review requested Feishu scopes before approval and grant only the permissions needed for the intended workflow. <br>
Risk: The skills rely on local command execution to run Node.js scripts. <br>
Mitigation: Install only from a trusted publisher and avoid disabling execution confirmations globally outside the intended agent environment. <br>
Risk: Some operations can modify or remove Feishu documents, sheets, bitables, drive files, tasks, calendars, or chat-related data. <br>
Mitigation: Require user confirmation for destructive or broad write operations and verify target document, table, folder, calendar, or record identifiers before execution. <br>
Risk: Document extraction behavior may install npm packages at runtime. <br>
Mitigation: Review runtime package installation behavior and run the skill in an environment where dependency installation is expected and monitored. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hashstacs-hk/feishu-skills) <br>
- [README](README.md) <br>
- [Feishu permissions guide](feishu-quick-setup/references/feishu-permissions.md) <br>
- [Feishu troubleshooting guide](feishu-quick-setup/references/troubleshooting.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [EnClaws](https://github.com/hashSTACS-Global/EnClaws) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and single-line JSON command results from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, create, update, download, upload, or delete Feishu resources according to granted OAuth scopes and local configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
