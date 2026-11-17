## Description:

Know-Your-Customer verification via MasterPay Global. Submit personal data, upload identity documents, and track approval status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d9m1n1c](https://clawhub.ai/user/d9m1n1c)

### License/Terms of Use:

MIT-0

## Use Case:

External users and supporting agents use this skill to complete identity verification, upload KYC documents, update required profile and identity fields, and monitor approval status through MasterPay-backed API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit personal profile information, identity documents, and authenticated KYC requests to a configurable API destination.

Mitigation: Confirm the configured AIOT_API_BASE_URL is the intended trusted HTTPS service before use, and proceed with real identity documents only after privacy and retention terms are understood.

Risk: Profile updates, document uploads, and KYC submission may make persistent account changes.

Mitigation: Review all user-provided identity, address, phone, and document fields before calling submission or upload endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/d9m1n1c/skills/aiotnetwork-kyc-identity)
- [Default AIOT API Base URL](https://payment-api-dev.aiotnetwork.io)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request details and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid authenticated session for protected KYC, profile, document, wallet, and MasterPay operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
