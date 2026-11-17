## Description:

Automatically detects missed daily reports, regenerates missing ones, updates the index, and logs reflections for report catch-up management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colbertlee](https://clawhub.ai/user/colbertlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to detect missed workday daily reports, generate catch-up markdown reports, check report quality, update report indexes, and view multi-agent reporting status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included skill management helper can install, update, or uninstall OpenClaw skills and may change the agent environment beyond the daily-report workflow.

Mitigation: Avoid the helper unless environment changes are intended; prefer explicit trusted package names and review each install, update, or uninstall command before running it.

Risk: Catch-up scripts write reports, index entries, logs, state, and optional reflection notes using workspace paths defined in the artifact.

Mitigation: Review and adjust workspace paths before full-mode execution, and use detect or quiet modes first when checking for missed reports.

Risk: Automatically generated catch-up reports can describe system status but may not capture the actual work performed on missed days.

Mitigation: Review and edit generated reports before treating them as authoritative daily records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colbertlee/skills/daily-report-catchup)
- [Publisher profile](https://clawhub.ai/user/colbertlee)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown reports, terminal text, shell command guidance, configuration snippets, and generated HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write daily report files, report indexes, logs, state files, reflection notes, and dashboard HTML depending on the selected script mode.]

## Skill Version(s):

1.5.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
