## Description:

Assists park operations teams with daily work triage, tenant service management, follow-up tracking, local SQLite queries, and scheduled Tencent Docs synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to manage park enterprise service workflows such as customer lookup, fee follow-up, work-order dispatch, inventory checks, contract-renewal warnings, visit planning, and KPI reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle and mutate sensitive enterprise service data, including local SQLite and JSON records.

Mitigation: Review the skill before installation, back up Excel and SQLite data, and require transactional sync checks before enabling data writes.

Risk: Scheduled sync, daemon mode, and automatic WeCom pushes can send or update operational data without timely human review.

Mitigation: Keep scheduled automation disabled until webhook allowlisting, redaction, and explicit approval controls are configured.

Risk: Unpinned installation sources can make it harder to reproduce the reviewed release.

Mitigation: Install a pinned release matching the server release hash before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/enterprise-service-assistant)
- [README](artifact/README.md)
- [Installation Guide](artifact/knowledge/INSTALL.md)
- [Onboarding Guide](artifact/knowledge/ONBOARDING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with structured tables, inline commands, configuration examples, and Python code snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce operational summaries, reminders, setup instructions, reports, and local data-management guidance.]

## Skill Version(s):

3.6.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
