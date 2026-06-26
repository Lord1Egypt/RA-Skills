## Description: <br>
Enterprise-grade backup and recovery toolkit supporting file backup, database backup, incremental backup, scheduled tasks, and disaster recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and operators use this skill to create, schedule, and restore file and database backups. It supports backup planning for local files, MySQL, PostgreSQL, MongoDB, incremental archives, versioned rollback, and disaster recovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore operations can overwrite files or extract unsafe tar archives. <br>
Mitigation: Restore only trusted backups into a staging directory first, inspect archive contents, and verify source and destination paths before promoting data. <br>
Risk: Database backup commands require credentials that could grant broad access. <br>
Mitigation: Use least-privilege database accounts and avoid root or production admin credentials. <br>
Risk: Unpinned dependency ranges can change installed code over time. <br>
Mitigation: Install in a virtual environment with a reviewed lockfile or pinned dependency versions. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/backup-recovery-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backup paths, restore destinations, cron expressions, and database connection settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
