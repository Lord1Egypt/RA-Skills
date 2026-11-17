## Description:

Coordinates parsing, retrieval, and review agents to produce transparent CNC manufacturing quote reports with cost breakdowns and risk warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing teams and developers use this skill to parse CNC quote requests, retrieve comparable cases, assess quote risk, and generate a transparent quote report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quote request details and generated quote data may be logged or retained.

Mitigation: Run with controlled log retention, mask customer-sensitive quote inputs, and avoid shared logging sinks for customer data.

Risk: The workflow declares email and calendar notifications without clear user controls.

Mitigation: Disable notification integrations by default and enable them only after explicit configuration, recipient review, and customer-data handling approval.

Risk: Optional UniSkill behavior references a local skill path that may not be controlled in all environments.

Mitigation: Keep UniSkill disabled unless the referenced local path is trusted, reviewed, and pinned for the deployment environment.

Risk: Dependency installation is broad enough to drift across environments.

Mitigation: Pin PyYAML to an approved version before production deployment and rebuild from a reproducible lockfile or equivalent controls.

## Reference(s):

- [CNC Quote Workflow ClawHub page](https://clawhub.ai/timo2026/skills/cnc-quote-workflow)
- [Referenced CNC Quote System skill](https://clawhub.com/timo2026/cnc-quote-system)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown quote report with structured quote details, risk warnings, competitive comparison, and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fallback rule-only quote calculations and optional notification configuration.]

## Skill Version(s):

2.0.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
