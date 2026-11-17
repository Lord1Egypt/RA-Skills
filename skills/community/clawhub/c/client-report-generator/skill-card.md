## Description:

Generate professional client-facing reports from raw data, metrics, and KPIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, agencies, and business users use this skill to turn CSV, JSON, analytics exports, or raw metrics into client-ready performance, campaign, project status, and analytics reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML export can carry unsafe HTML or JavaScript into client-facing reports.

Mitigation: Prefer Markdown output, review generated HTML before sharing or hosting it, and avoid publishing HTML generated from untrusted content until escaping and link-scheme validation are fixed.

Risk: Generated client reports may include incorrect conclusions when source data is incomplete or untrusted.

Mitigation: Review metrics, assumptions, and recommendations against the source data before client delivery.

## Reference(s):

- [Report Templates](references/report-templates.md)
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/client-report-generator)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports by default, with optional HTML, plain text, and JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can parse CSV, TSV, and JSON inputs into normalized metrics; HTML export uses inline CSS themes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
