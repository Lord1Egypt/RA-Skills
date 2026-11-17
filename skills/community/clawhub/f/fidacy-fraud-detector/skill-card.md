## Description:

Verifies Fidacy-signed payment or approval verdicts before an agent acts, helping detect forged or tampered approval claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fidacy](https://clawhub.ai/user/fidacy)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent operators use this skill to verify signed Fidacy verdicts received from external agents or services before proceeding with payment, approval, or other consequential actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment or approval decisions could rely on an unpinned external verifier dependency or overly broad issuer trust.

Mitigation: Pin and review @fidacy/verify, restrict JWKS fetching to trusted HTTPS issuer endpoints, and define accepted issuers and freshness windows before use.

## Reference(s):

- [Fidacy public JWKS](https://api.fidacy.com/.well-known/jwks.json)
- [Fidacy signup](https://app.fidacy.com/signup)
- [ClawHub skill page](https://clawhub.ai/fidacy/skills/fidacy-fraud-detector)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to verify JWS verdicts, gate actions on verification results, and configure trusted issuers, keys, and freshness windows.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
