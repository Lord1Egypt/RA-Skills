## Description:

Cofferline helps agents manage on-chain treasury operations and Polymarket risk controls over a REST API, including funding, gas, conversions, spend policies, scoped signing delegation, USDC payments, order routing, and audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guscoffer](https://clawhub.ai/user/guscoffer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill when an autonomous agent needs wallet-based treasury management, policy-bounded crypto execution, Polymarket order handling, or auditable accounting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through high-impact crypto treasury and prediction-market workflows.

Mitigation: Use it only for intended crypto or prediction-market operations, verify the manifest and terms before use, and configure conservative spend and trading policies.

Risk: Mis-scoped credentials or delegations could grant more authority than the operator intended.

Mitigation: Use the least privileged API key scope, avoid sharing funds keys, and confirm revocation paths for delegations, venue credentials, and auto-topup authorizations before deployment.

Risk: Prepaid fee balances, pre-signed auto-topup authorizations, and optional venue credentials are exceptions to the non-custodial wallet model.

Mitigation: Review the custody matrix and keep platform-held balances, stored authorizations, and venue credential permissions limited to the workflow's actual needs.

## Reference(s):

- [Cofferline manifest](https://cofferline.com/.well-known/cofferline.json)
- [Cofferline Skill on ClawHub](https://clawhub.ai/guscoffer/skills/cofferline)
- [Publisher profile](https://clawhub.ai/user/guscoffer)

## Skill Output:

**Output Type(s):** [guidance, API Calls, shell commands, configuration]

**Output Format:** [Markdown with REST API examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce policy, authentication, payment, delegation, trading, and accounting instructions for a connected agent workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
