## Description:

Scores Cainiao logistics suppliers and Cainiao station operators for risk, then produces a structured report with risk level, core issue diagnosis, and recommended actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal control and supplier-management teams use this skill to assess Cainiao logistics suppliers and station operators from KPI, complaint, violation, and operating-history data. The output supports advisory review of whether a counterparty is low risk, needs monitoring, or requires escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scores may be unreliable when underlying Cainiao rules, referenced documents, or input KPI data are missing, stale, or self-reported.

Mitigation: Verify the applicable Cainiao rules and referenced documents, label missing data, and prefer platform data before relying on the assessment.

Risk: Risk recommendations may influence suspension, termination, or other consequential supplier and station decisions.

Mitigation: Treat the report as advisory and require human review before suspension, termination, or clearing actions.

Risk: Complaint records, KPI reports, and violation descriptions may contain personal or confidential information.

Mitigation: Avoid uploading unnecessary personal or confidential data, and minimize or redact sensitive inputs where possible.

## Reference(s):

- [Continuation Reference](artifact/references/continuation.md)
- [Glossary](docs/GLOSSARY.md)
- [Insufficiency Handling](docs/INSUFFICIENCY-HANDLING.md)
- [Rule Update SOP](docs/RULE-UPDATE-SOP.md)
- [ClawHub Skill Page](https://clawhub.ai/nic-yuan/skills/02-risk-scoring)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk scoring report with tables, score breakdowns, diagnosis, recommended actions, warnings, and review timing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for missing required inputs, labels data gaps, and treats scores as advisory rather than final decisions.]

## Skill Version(s):

1.0.0 (source: server release evidence); artifact frontmatter reports 1.7.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
