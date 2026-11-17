## Description:

05 Monthly Report helps agents draft structured monthly internal-control compliance reports from complaint, logistics exception, supplier, station, and major incident data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal compliance and operations teams use the skill to turn monthly complaint, exception, supplier, station, and incident data into a management-facing compliance report with trends, gaps, and next-month priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monthly compliance inputs may include personal data, customer identifiers, confidential legal material, or sensitive incident details.

Mitigation: Use aggregated or redacted data where possible and provide sensitive details only under approved organizational handling rules.

Risk: Incomplete inputs can lead to a simplified or limited report that may not support management decisions on its own.

Mitigation: Label data gaps clearly, use the skill's data-insufficient mode when minimum inputs are missing, and review the report before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/05-monthly-report)
- [Glossary](docs/GLOSSARY.md)
- [Insufficiency handling](docs/INSUFFICIENCY-HANDLING.md)
- [Rule update SOP](docs/RULE-UPDATE-SOP.md)
- [Linking SOP](docs/LINKING-SOP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided monthly operational data and may produce simplified or data-insufficient reports when required inputs are incomplete.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
