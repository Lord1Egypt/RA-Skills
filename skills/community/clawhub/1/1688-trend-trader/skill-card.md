## Description:

1688 爆款操盘手 helps agents analyze product opportunities, search 1688 suppliers, draft supplier inquiries, calculate margins, and assemble sourcing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skovely](https://clawhub.ai/user/skovely)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, sourcing operators, and agent users use this skill to identify 1688 product opportunities, compare factories, prepare negotiation and inquiry scripts, and estimate cross-border commerce margins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to 1688 domains during sourcing and product lookup workflows.

Mitigation: Run it only in environments where outbound access to the declared 1688 domains is acceptable, and review returned supplier data before acting on it.

Risk: The security evidence says the skill under-discloses optional use of ALI_COOKIE for authenticated 1688 access.

Mitigation: Do not set ALI_COOKIE unless authenticated 1688 session use is intentional; prefer the declared ALI_APP_KEY and ALI_APP_SECRET configuration for enhanced data access.

Risk: Sourcing recommendations can miss product-specific patent, certification, logistics, or marketplace-compliance requirements.

Mitigation: Use the generated risk prompts as a checklist and verify intellectual property, certification, and shipping constraints with qualified reviewers before purchase or launch.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skovely/skills/1688-trend-trader)
- [Selection Analysis Reference](artifact/references/selection.md)
- [Factory Sourcing Standards](artifact/references/sourcing.md)
- [Inquiry Template Library](artifact/references/inquiry.md)
- [Financial Calculation Reference](artifact/references/financial.md)
- [Supply Chain Report Template](artifact/references/report-template.md)
- [1688 Open Platform](https://open.1688.com/)
- [1688 Open API Gateway](https://gw.open.1688.com/openapi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with structured sections, supplier comparison tables, inquiry scripts, calculations, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first sourcing workflow; outputs emphasize evidence-backed supplier metrics, margin figures, and practical next steps.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
