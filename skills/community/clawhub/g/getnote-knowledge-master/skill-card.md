## Description: <br>
Get笔记·六步抄作业版 helps an agent run a six-step Get笔记 knowledge-management workflow for creating knowledge bases, saving content, organizing notes, searching, saving analyses, and producing health reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhuatochina](https://clawhub.ai/user/binhuatochina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Get笔记 through CLI-first knowledge workflows: creating libraries, saving links or text, organizing notes, searching semantically, preserving analysis results, and reviewing knowledge-base coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Get笔记 credentials and can access large portions of a user's private notes. <br>
Mitigation: Install only when that access is intended, scope credentials where possible, and confirm the target knowledge base before broad reads or writes. <br>
Risk: The workflow can save, tag, or delete note content and may publish summaries to Feishu destinations. <br>
Mitigation: Require explicit confirmation for every write, duplicate deletion, Feishu destination, and publication step. <br>
Risk: The Cron workflow can run recurring broad scans, create local archives, save reports to Get笔记, and send Feishu notifications. <br>
Mitigation: Enable Cron behavior only when recurring scans and publication are intentional, and review its configured destinations before use. <br>


## Reference(s): <br>
- [卡帕西六步抄作业法 · Get笔记落地手册](references/6steps.md) <br>
- [Get笔记 OpenAPI endpoint](https://openapi.biji.com) <br>
- [ClawHub skill page](https://clawhub.ai/binhuatochina/getnote-knowledge-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute Get笔记 CLI/API operations that read, write, tag, or summarize notes when credentials and user confirmation are available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
