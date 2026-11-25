## Description:

Guides developers in creating hosted Didit KYC workflows and sessions, generating verification links, and retrieving verification decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate identity verification into backend or API-key flows, send users through hosted document and selfie checks, and retrieve the resulting decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a session-linked face blocklist action that may be unexpected, and notes that analysis was partial.

Mitigation: Before installing, confirm the blocklist behavior is expected, review the declared scope and the data and credentials sent to Didit, and account for the incomplete analysis.

## Reference(s):

- [Didit documentation](https://docs.didit.me)
- [Create workflows](https://docs.didit.me/management-api/workflows/create)
- [Workflow feature configurations](https://docs.didit.me/management-api/workflows/feature-configs)
- [Create sessions](https://docs.didit.me/sessions-api/create-session)
- [Retrieve verification decisions](https://docs.didit.me/sessions-api/retrieve-session)
- [Verification statuses](https://docs.didit.me/integration/verification-statuses)
- [Programmatic registration](https://docs.didit.me/integration/programmatic-registration)
- [Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Markdown with Python examples and JSON API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Didit API key supplied through DIDIT_API_KEY.]

## Skill Version(s):

1.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
