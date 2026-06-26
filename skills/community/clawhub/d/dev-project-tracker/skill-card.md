## Description: <br>
Dev Project Tracker helps agents manage requirement- or version-based software project lifecycles by creating project folders, recording progress, tracking issues, managing changes, and supporting distillation and archival workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project leads use this skill to maintain local project-tracking folders for requirement-based software iterations, including progress logs, issue tables, change records, project status summaries, and archive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project progress, decisions, and personnel details may be written to logs or long-term memory. <br>
Mitigation: Avoid confidential personnel or project details unless persistent storage is acceptable, and review what the agent records. <br>
Risk: Archive workflows may delete an original project directory after compressing it into an archive summary. <br>
Mitigation: Require explicit owner confirmation before any archive step that deletes original project files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangliujiao-tal/dev-project-tracker) <br>
- [Project overview template](references/templates/README.md) <br>
- [Work log template](references/templates/WORK_LOG.md) <br>
- [Issue tracking template](references/templates/ISSUES.md) <br>
- [Change record template](references/templates/CHANGES.md) <br>
- [Division template](references/templates/DIVISION.md) <br>
- [Design document template](references/templates/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown project files, directory paths, status summaries, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local project documentation and propose distillation or archive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
