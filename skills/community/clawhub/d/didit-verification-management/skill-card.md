## Description:

Use this skill to write backend or API-key integrations for managing Didit's identity verification platform, including account setup, workflows, verification sessions, KYC and KYB records, billing, lists, and webhook signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to set up Didit accounts and manage KYC/KYB workflows, identity sessions and records, billing, and webhook handling through the Didit APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook freshness and unsigned callback handling may allow untrusted or stale event data to influence decisions.

Mitigation: Check timestamps and HMAC signatures where provided; for documented unsigned callbacks, verify the request identifier and confirm current state through the authenticated Didit API before acting.

Risk: Migration of identity records can expose personal or biometric data when retention and deletion choices are unclear.

Mitigation: Define access, retention, and deletion rules before migration; use privacy erasure and purge retained biometric templates when required.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Management API Overview](https://docs.didit.me/sessions-api/management-api)
- [API Keys](https://docs.didit.me/console/api-keys)
- [Webhook Integration Guide](https://docs.didit.me/integration/webhooks)
- [Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration guidance, Integration guidance]

**Output Format:** [Markdown with Python examples, API request examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Python helper scripts; API operations require Didit credentials such as DIDIT_API_KEY.]

## Skill Version(s):

5.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
