## Description:

Decentralized identity (DID) management, on-chain KYC status, and membership tiers with token staking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d9m1n1c](https://clawhub.ai/user/d9m1n1c)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check or create a decentralized identity, complete on-chain KYC, review membership tiers, and stake tokens for membership upgrades through the AIOT Network API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide identity verification and token-staking actions that may be sensitive or difficult to reverse.

Mitigation: Require explicit user confirmation before DID creation, KYC completion, or token staking, and explain that DID creation is one-time before execution.

Risk: API calls rely on the configured AIOT endpoint and authenticated user context.

Mitigation: Use only a trusted AIOT_API_BASE_URL value and verify a valid bearer token before calling authenticated endpoints.

Risk: Transaction PINs and authentication secrets may be needed during workflows.

Mitigation: Ask for transaction PINs fresh each time and do not cache, log, expose, or persist passwords, tokens, PINs, card numbers, or CVVs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/d9m1n1c/skills/aiotnetwork-blockchain-did)
- [Publisher Profile](https://clawhub.ai/user/d9m1n1c)
- [AIOT Network API Base URL](https://payment-api-dev.aiotnetwork.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API call instructions]

**Output Format:** [Markdown with inline shell commands and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated bearer token for protected API operations and AIOT_API_BASE_URL configuration when overriding the default endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
