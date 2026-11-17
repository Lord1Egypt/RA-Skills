## Description:

Assesses GDPR compliance readiness and generates gap analysis with remediation guidance for data privacy, EU data protection, privacy impact assessment, data subject rights, consent management, and international transfer reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security, privacy, and compliance teams use this skill to collect GDPR readiness details and generate a compliance score, gap analysis, and prioritized remediation guidance. It is intended for organizations evaluating GDPR controls, data subject rights handling, consent management, breach procedures, vendor agreements, and international transfer practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organization name, GDPR controls, data categories, transfer practices, and compliance gaps to a third-party API.

Mitigation: Use only after organizational approval of ToolWeb privacy and data-processing terms; redact or generalize sensitive answers where possible.

Risk: The API key enables billable ToolWeb API calls and may expose account access if shared broadly.

Mitigation: Use a limited API key, scope access to approved agents, and rotate the key if it is exposed.

Risk: Generated compliance guidance may be incomplete for regulated or high-impact decisions.

Mitigation: Review outputs with qualified privacy, legal, or compliance staff before using them for audit, reporting, or remediation commitments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/gdpr-compliance-tracker)
- [ToolWeb API portal](https://portal.toolweb.in)
- [GDPR tracker API endpoint](https://portal.toolweb.in/apis/compliance/gdpr-tracker)
- [ToolWeb platform](https://toolweb.in)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style GDPR compliance assessment with score, compliant areas, critical gaps, and prioritized actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; sends assessment inputs to portal.toolweb.in for API-backed analysis.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
