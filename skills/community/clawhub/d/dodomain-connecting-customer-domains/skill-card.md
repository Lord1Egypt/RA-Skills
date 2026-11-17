## Description:

Helps users connect a customer's domain to their app through doDomain, provide the required DNS records, and verify the connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and customer-facing teams use this skill to connect a customer's domain to an app, share the DNS records to configure, and check whether those records have been verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a connection consumes monthly quota.

Mitigation: Confirm the app, domain, records, and user approval before creating at most one session per domain per request.

Risk: Incorrect DNS records can delay verification.

Mitigation: Do not invent record targets; present the required records and check each record before reporting verification.

Risk: Connect sessions return a session token.

Mitigation: Share the token only with the requesting user and reuse an existing session for progress checks.

## Reference(s):

- [Connecting Customer Domains on ClawHub](https://clawhub.ai/devino/skills/dodomain-connecting-customer-domains)

## Skill Output:

**Output Type(s):** [Text, Configuration guidance]

**Output Format:** [Markdown with DNS record details and verification status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a connect session token and per-record verification results when available.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
