## Description: <br>
飞书云盘 AI 管家 helps an agent organize Feishu Drive files and folders through bulk organization, automatic classification, file search, storage reports, and comment management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[young-joey](https://clawhub.ai/user/young-joey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams using Feishu Drive can ask an agent to classify files, manage folders, find stale or misplaced documents, produce storage reports, and manage file comments. The skill is suited to scoped cloud-drive cleanup and reporting workflows where the user reviews planned file changes before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk moves, archiving, deletes, or comment actions can change many Feishu Drive items at once. <br>
Mitigation: Ask the agent for a dry-run list, confirm the exact folder scope, and approve the planned changes before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/young-joey/feishu-drive-organizer) <br>
- [Feishu Drive operation reference](references/drive-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown guidance, file lists, folder plans, storage reports, and Feishu Drive API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions may include listing folders, creating folders, moving files, soft-deleting files, and reading or writing comments when authorized by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
