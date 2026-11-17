## Description:

Assess compliance with India's Digital Personal Data Protection (DPDP) Act 2023 across 7 domains with 41 controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and compliance teams use this skill to gather DPDP assessment inputs for organizations operating in India and receive a maturity score, domain-level analysis, checklist, remediation roadmap, and executive summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organization DPDP readiness details to ToolWeb.in through a third-party, billable API.

Mitigation: Use only with authorization to disclose the organization's compliance posture, confirm quota or billing impact, and avoid submitting secrets, incident evidence, internal hostnames, personal data, or confidential free-text details.

Risk: Assessment output may influence privacy and compliance decisions for organizations operating in India.

Mitigation: Review the generated findings and roadmap with qualified privacy, legal, or security stakeholders before relying on them for formal compliance decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/dpdp-compliance-assessment)
- [ToolWeb Portal](https://portal.toolweb.in)
- [ToolWeb DPDP Compliance API](https://portal.toolweb.in/apis/compliance/dpdp-compliance)
- [ToolWeb Platform](https://toolweb.in)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style assessment summary with scores, domain analysis, critical gaps, checklist items, remediation roadmap, and executive summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may consume quota or incur billing through ToolWeb.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
