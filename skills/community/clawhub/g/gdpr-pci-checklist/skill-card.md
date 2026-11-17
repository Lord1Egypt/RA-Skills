## Description:

Generate customized compliance checklists for GDPR and PCI-DSS standards based on company type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance teams, security officers, developers, and organizations handling customer data or payment information use this skill to request tailored GDPR and PCI-DSS checklist items for audit preparation, risk assessment, and compliance program planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submitted company type is sent to the provider's external API.

Mitigation: Use broad company classifications and avoid entering sensitive internal details unless the provider's terms and data handling meet organizational requirements.

Risk: Generated checklist items may be incomplete for a specific legal, regulatory, or audit context.

Mitigation: Have qualified compliance, security, or legal reviewers validate checklist items before relying on them for audit readiness or policy decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/gdpr-pci-checklist)
- [Publisher Profile](https://clawhub.ai/user/krishnakumarmahadevan-cmd)
- [OpenAPI Specification](artifact/openapi.json)
- [API Docs](https://api.mkkpro.com:8015/docs)
- [API Route](https://api.mkkpro.com/compliance/gdpr-pci-checklist)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [External API call sends the submitted company_type value to the provider service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
