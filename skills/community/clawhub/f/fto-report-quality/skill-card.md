## Description:

Reviews existing freedom-to-operate and patent infringement risk reports, scores their search, analysis, legal reasoning, and documentation quality, and produces standardized HTML assessment reports with optional validation outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, patent, and product teams use this skill to review existing FTO, patent infringement risk, or exhibition IP risk reports before relying on them for launch, export, bidding, licensing, or internal compliance decisions. The skill helps an agent create structured quality findings, score report completeness, and generate decision-support artifacts for human legal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated legal-risk reports may be mistaken for final legal advice.

Mitigation: Treat every generated report as a draft decision-support artifact and require review by qualified legal or patent professionals before business use.

Risk: Generated HTML reports may include unsafe or unvalidated patent-result links.

Mitigation: Validate or strip patent-result links before sharing reports outside the review environment.

Risk: Advertised v9 recall, fatal-defect, and safeguard behavior may not fully match the shipped scripts.

Mitigation: Test the scripts against real PatSnap data and update them before relying on those safeguards for production decisions.

## Reference(s):

- [FTO Report Quality Assessment Checklist](artifact/references/assessment-checklist.md)
- [FTO Report Quality Standards Manual](artifact/references/fto-quality-standards.md)
- [Harness Check Catalog](artifact/references/harness-checks.md)
- [Independent Verification Guide for FTO Review](artifact/references/independent-verification-guide.md)
- [FTO Report Quality Assessment Template](artifact/assets/assessment-report-template.md)
- [ClawHub Skill Release Page](https://clawhub.ai/yuanzhian-patsnap/skills/fto-report-quality)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, HTML files, JSON]

**Output Format:** [HTML report files with optional JSON and HTML validation reports, plus concise agent guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are decision-support drafts for human review; report generation uses fixed CSS and the optional harness is run only when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact docs state v9.0 method version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
