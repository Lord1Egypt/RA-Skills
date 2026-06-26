## Description: <br>
Organize and maintain AI agent workspaces with structured directories, clear naming, regular audits, dead file detection, and safe cleanup practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[briandavisbikes-code](https://clawhub.ai/user/briandavisbikes-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to organize AI agent workspaces, audit local files, classify active and archived content, identify dead file candidates, and plan safe cleanup work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output can include local workspace file paths and file sizes. <br>
Mitigation: Review and redact audit output before sharing it outside the workspace. <br>
Risk: Cleanup guidance could be misapplied to files that are still active. <br>
Mitigation: Verify cron, script, skill, and agent references before cleanup; create a commit or rollback point and use recoverable deletion. <br>
Risk: Dead file candidates are heuristic and not proof that a file is unused. <br>
Mitigation: Treat candidates as manual review prompts and confirm them with the documented grep and cron checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/briandavisbikes-code/file-management-by-brian) <br>
- [File Management Skill](artifact/SKILL.md) <br>
- [File Management Reference](artifact/FILE-MANAGEMENT.md) <br>
- [Workspace Audit Script](artifact/audit-workspace.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional shell script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local workspace paths, file sizes, and cleanup candidates when the audit script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
