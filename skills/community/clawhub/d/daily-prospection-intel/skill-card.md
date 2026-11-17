## Description:

Generates a daily .docx commercial intelligence report identifying eight recent European pharma regulatory opportunities for ArcaScience's BRA platform, with target narratives and outreach email drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomus42](https://clawhub.ai/user/atomus42)

### License/Terms of Use:

MIT-0

## Use Case:

Commercial, business development, and regulatory teams use this skill to produce a daily European regulatory opportunity report for ArcaScience's benefit-risk assessment platform. It supports prospecting by combining recent regulatory research, target prioritization, ArcaScience positioning, and draft outreach emails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rely on broad private dossier paths outside the workspace.

Mitigation: Replace configured local dossier paths with reviewed, workspace-scoped data sources before use.

Risk: Scheduled execution can run prospecting work without enough user control.

Mitigation: Require confirmation or an approved schedule before recurring runs are enabled.

Risk: Generated outreach emails may contain inaccurate, outdated, or overconfident claims.

Mitigation: Treat every outreach email as a draft and require human review before sending.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atomus42/skills/daily-prospection-intel)
- [ArcaScience Company Context & Positioning](references/arcascience-context.md)
- [ArcaScience Sales Package - Platform & Product Reference](references/sales-package-platform.md)
- [ArcaScience Sales Package - Client Proposals & BRA Analysis](references/sales-package-proposals.md)
- [ArcaScience Sales Package - Buyer Personae Analysis](references/sales-package-personae.md)
- [ArcaScience Sales Package - Operations & Contracts](references/sales-package-operations.md)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Guidance]

**Output Format:** [.docx report with structured target analysis and draft outreach email templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves a dated ArcaScience_Daily_Intel_YYYYMMDD.docx report to the workspace; generated outreach content requires human review before use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
