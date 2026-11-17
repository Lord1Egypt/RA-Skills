## Description:

Guides agents through customer complaint intake, classification, time-bound handling, closure, follow-up, and reporting for property service workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT

## Use Case:

Property service and customer service teams use this skill to standardize complaint intake, severity classification, response tracking, follow-up, and recurring complaint analysis. It supports operational workflows that require 30-minute response targets, 7-day closure targets, escalation handling, and customer callback management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle sensitive customer complaint records and generated reports or backups.

Mitigation: Install only in an authorized complaint-management environment, restrict access to generated reports and backups, minimize personal data, and define clear retention policies.

Risk: Complaint details may be sent through WeCom notification webhooks if notification behavior is configured.

Mitigation: Configure WeCom destinations deliberately, verify recipient groups before use, and avoid sending unnecessary personal or sensitive complaint details.

Risk: Spreadsheet-backed complaint records may contain user-provided values.

Mitigation: Neutralize spreadsheet formula-like values before writing or exporting complaint data.

Risk: Local paths for complaint data, reports, backups, and configuration must match the deployment environment.

Mitigation: Review and configure file paths before use so records are read from and written to approved storage locations.

## Reference(s):

- [Complaint Handling skill page](https://clawhub.ai/perrykono-debug/skills/complaint-handling)
- [Skill source documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, console text, JSON reports, Python code, shell-command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update complaint records, reminders, backups, and reports when connected to local complaint data and configured notification channels.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
