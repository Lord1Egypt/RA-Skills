## Description:

Dev Project Tracker helps agents create and maintain per-requirement project documentation, including progress logs, issue tracking, change records, lifecycle status, and archival summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to organize software project requirements by version or feature, keep project records current, and summarize status across active work. It is intended for project documentation workflows that need repeatable templates, progress tracking, issue management, and controlled archival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project updates, decisions, and personnel details may be persisted outside project files in long-term memory.

Mitigation: Require explicit approval for memory writes, avoid sensitive personnel details unless necessary, and review retention expectations before use.

Risk: Archival behavior may delete original project directories after compression into an archive summary.

Mitigation: Require an exact deletion-target preview, responsible-owner confirmation, and a recoverable archive or backup before removing project directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangliujiao-tal/skills/dev-project-tracker)
- [Project README template](artifact/references/templates/README.md)
- [Work log template](artifact/references/templates/WORK_LOG.md)
- [Issue tracker template](artifact/references/templates/ISSUES.md)
- [Change record template](artifact/references/templates/CHANGES.md)
- [Division template](artifact/references/templates/DIVISION.md)
- [Design document template](artifact/references/templates/DESIGN.md)
- [Project status scan script](artifact/scripts/scan-projects.sh)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown project documents, directory structures, status summaries, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project documentation files and produce lifecycle summaries for active, distillation, and archived project states.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
