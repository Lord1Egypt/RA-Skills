## Description: <br>
Backup and restore Daniel agents with git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators use this skill to set up, audit, repair, and restore backup continuity for Daniel-owned agents. It guides agents through preserving durable memory and workspace source files in git while restoring secrets through approved secret-management paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secrets, credentials, runtime artifacts, or private/customer data could be committed to git during backup. <br>
Mitigation: Review staged files before each commit, keep credentials outside git, and use a .gitignore that blocks env files, auth stores, logs, caches, databases, and bulky generated state. <br>
Risk: Backups could be pushed to the wrong repository or a repository without appropriate ownership or access controls. <br>
Mitigation: Confirm the Azure DevOps organization, project, repo, and credential method before first push, and ask Daniel before creating repositories, changing access controls, or pushing to a new remote. <br>
Risk: Git backups may be mistaken for full machine recovery. <br>
Mitigation: Use git for durable human-readable memory and configuration only; restore secrets through approved secret paths and rely on system-level backups for full runtime recovery. <br>


## Reference(s): <br>
- [DR Agent Backup on ClawHub](https://clawhub.ai/daniel-refahi-ikara/skills/dr-agent-backup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklist steps and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, commit, restore, and audit procedures for git-based agent continuity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
