## Description:

Monitors ADC R&D, clinical evidence, patents, licensing deals, approvals, literature, and conference activity to generate periodic landscape briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

ADC R&D and business-development teams use this skill to track recent clinical, patent, deal, approval, literature, and competitive events and turn them into weekly, monthly, or custom-range monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates interactive HTML reports from external ADC-related data, and the security evidence says explicit escaping, sanitization, safe URL validation, and browser defenses are not clear.

Mitigation: Review generated reports as untrusted documents and confirm that externally sourced content is escaped, sanitized, and linked through validated URLs before sharing or opening in sensitive environments.

Risk: The security verdict is suspicious because the skill runs external ADC-related searches and creates local HTML reports.

Mitigation: Install and run it only in environments where external search activity and local report generation are acceptable, and review outputs before relying on them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/adc-landscape-monitoring)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Self-contained HTML report with structured summaries, source links, filters, statistics, and visual sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may cover weekly, monthly, or custom date ranges and include downloadable HTML output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
