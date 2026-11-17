## Description:

Queries land ownership, leases, landlord information, and land payments, and supports authenticated payment-management and lease-renewal operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianppetty](https://clawhub.ai/user/brianppetty)

### License/Terms of Use:


## Use Case:

Authorized farm operations employees and managers use this skill to review land portfolios, lease status, landlord details, annual land costs, and payment obligations, and to carry out controlled payment and lease-renewal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive landlord, lease, and payment data in a business system.

Mitigation: Use it only with protected FarmOS API deployments that enforce server-side authentication, TLS, and least-privilege tokens.

Risk: A local role file is not sufficient as the only access boundary for sensitive portfolio data.

Mitigation: Enforce admin or manager authorization on the server before returning land, landlord, lease, or payment data.

Risk: Bulk payment marking, lease renewals, and year-end rollover actions can change business records at scale.

Mitigation: Require preview, explicit user confirmation, and authenticated requests before executing bulk or year-end changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianppetty/skills/farmos-land-portfolio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should state record counts for complete data retrieval and require preview and confirmation before bulk write operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
