## Description:

Verifies Australian business registration details against the Australian Business Register using an ABN, ACN, or entity name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to verify ABN, ACN, entity name, registration status, GST status, entity type, location, and trading names for Australian supplier onboarding, invoice checks, KYC, compliance, and due-diligence workflows.

### Deployment Geography for Use:

Global, for Australian business registration checks

## Known Risks and Mitigations:

Risk: Live lookups send the queried ABN, ACN, or business name to the Australian Business Register.

Mitigation: Tell users what will be queried before lookup when context is sensitive, and avoid submitting unrelated confidential information.

Risk: ABR results verify register status but are not a complete fraud, credit, or due-diligence decision.

Mitigation: Present results as register verification and recommend additional checks for high-value, regulated, or suspicious transactions.

Risk: The ABR GUID is a credential-like setup value that could be exposed if pasted into chat or logs.

Mitigation: Store the GUID only in the ABR_GUID environment variable and do not print, hardcode, or ask the user to paste it into chat.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arbazex/skills/australian-business-verification)
- [ABR Web Services Registration](https://abr.business.gov.au/Tools/WebServices)
- [ABR JSON API Reference](reference/api-reference.md)
- [ABR Entity Type Codes](reference/entity-types.md)
- [Example Responses](examples/sample-responses.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain-language summaries, Markdown guidance, inline shell commands, and JSON helper-script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ABR_GUID for live ABR lookups; local ABN and ACN checksum validation can run without a network call.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
