## Description:

Tracks and summarizes daily AI-service revenue by logging transactions, generating Markdown reports, and analyzing income by source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthasking123](https://clawhub.ai/user/arthasking123)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this local CLI tracker to record AI-service income, check daily and cumulative totals, and generate daily Markdown summaries for business review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Revenue entries and generated reports are stored in local files.

Mitigation: Run the tracker only in a trusted workspace and manage access to the logs/ and reports/ directories.

Risk: Untrusted source or description text can appear unsanitized in generated Markdown reports.

Mitigation: Avoid logging untrusted text, validate entry fields before recording them, and review generated reports before sharing or using them for decisions.

Risk: Malformed or incorrect amounts can affect daily and cumulative revenue totals.

Mitigation: Validate amounts before entry and reconcile generated summaries against source records before relying on them for business reporting.

## Reference(s):

- [AI Revenue Tracker ClawHub page](https://clawhub.ai/arthasking123/skills/ai-revenue-tracker)
- [Skill documentation](artifact/SKILL.md)
- [Sample daily summary report](artifact/reports/daily_summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [CLI text output and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local revenue logs and daily summary reports under logs/ and reports/.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
