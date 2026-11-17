## Description:

Turns audit findings into stakeholder-ready Markdown or CSV reports with severities, affected-page counts, history, and evidence labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO teams, and site owners use this skill to package validated site-audit findings into shareable reports. It emphasizes grouped root causes, severity, affected-page counts, evidence history, and clear SHIP/FIX/BLOCK/UNDECIDED verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run an unbundled local Python validator from a dynamically located skills root, creating local code execution risk.

Mitigation: Install only in trusted Groundcrew environments and verify the skills root and .groundcrew/groundcrew-doctor.py before relying on validator results.

Risk: Optional SEO and analytics connectors may share site data with third-party services when enabled.

Mitigation: Use connectors only when the user has authorized the provider and keep API keys and secrets out of generated reports.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Connectors and categories](artifact/references/connectors.md)
- [Reporting contract](artifact/references/reporting.md)
- [WHY-NOT-SLOP doctrine](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md)
- [Groundcrew ethics](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md)

## Skill Output:

**Output Type(s):** [Markdown, CSV, Files, Guidance]

**Output Format:** [Markdown report and optional CSV findings table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SHIP/FIX/BLOCK/UNDECIDED verdicts and labels reported values as Measured, User-provided, or Estimated.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
