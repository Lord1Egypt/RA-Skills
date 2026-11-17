## Description:

This skill helps users plan, record, and review household or office cleaning tasks, including checklists, supply inventory, local SQLite history, cleaning tips, and monthly HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage routine home or office cleaning work: generate room-based plans, record completed work, track cleaning supplies, search cleaning guidance, and create monthly visual reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated monthly reports may execute unsafe HTML or JavaScript and load Chart.js from a third-party CDN.

Mitigation: Review generated reports before opening them, avoid untrusted text in cleaning records, and prefer a version that escapes report fields and bundles Chart.js locally with integrity controls.

Risk: Cleaning records and supply inventory are stored locally in SQLite and may contain household or office routine data.

Mitigation: Install only where local storage is acceptable, avoid sensitive personal details in records, and apply normal device and file-access protections to the skill data directory.

Risk: The skill supports saves and deletes for records, checklists, and supplies.

Mitigation: Confirm destructive actions before execution and keep backups of the local database when records need to be retained.

Risk: The report writer accepts an optional output path.

Mitigation: Restrict report output to the skill data directory unless the user explicitly chooses another trusted location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/cleaning-assistant)
- [Skill homepage from metadata](https://github.com/bettermen/cleaning-assistant)
- [Chart.js CDN used by generated reports](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with shell commands, JSON CLI output, SQLite-backed local files, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local SQLite data under the skill data directory; monthly reports are written as HTML files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
