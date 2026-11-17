## Description:

Validate URLs and JSON schemas against format rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:


## Use Case:

Developers and agents use Data Validate to check URL, JSON Schema, email, and phone-number formats through an external validation service after obtaining user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation inputs are sent to an external validation service.

Mitigation: Obtain explicit user consent before sending user-provided data to validate.agentutil.net.

Risk: Secrets, regulated records, private JSON payloads, or sensitive personal contact data could be submitted for validation.

Mitigation: Avoid submitting sensitive data unless consent and compliance requirements have been confirmed.

Risk: The service performs syntax and format checks only, not semantic verification.

Mitigation: Treat successful responses as format validation only, not proof that an email inbox, phone number, payment network, or external account exists.

## Reference(s):

- [Data Validate on ClawHub](https://clawhub.ai/cutthemustard/skills/data-validate)
- [Validation service homepage](https://validate.agentutil.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user consent before sending validation input to validate.agentutil.net; no authentication is required for the free tier.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
