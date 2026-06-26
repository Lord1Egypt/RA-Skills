## Description: <br>
Organize and maintain AI agent workspaces using structured directories, clear naming, regular audits, and safe cleanup of unused or dead files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[briandavisbikes-code](https://clawhub.ai/user/briandavisbikes-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to organize OpenClaw or similar AI agent workspaces, audit files, identify cleanup candidates, and follow safer cleanup practices before restructuring or removing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output can expose private filenames, logs, workspace paths, sizes, and timestamps. <br>
Mitigation: Run audits only on workspaces intended for review and avoid sharing raw audit output without checking it for sensitive local details. <br>
Risk: Cleanup guidance may lead to accidental loss if files are removed before references and backups are checked. <br>
Mitigation: Treat cleanup steps as manual actions, verify cron and script references, and create a backup or git savepoint before removing files. <br>


## Reference(s): <br>
- [File Management reference](artifact/FILE-MANAGEMENT.md) <br>
- [Workspace audit script](artifact/audit-workspace.sh) <br>
- [ClawHub skill page](https://clawhub.ai/briandavisbikes-code/briandavis-file-mgmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local audit script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, sizes, timestamps, workspace structure, and manually reviewed cleanup candidates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
