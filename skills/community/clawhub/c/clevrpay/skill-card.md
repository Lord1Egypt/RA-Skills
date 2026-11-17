## Description:

Clevr Pay helps agents guide trusted stablecoin payment workflows, including A-Pass checks, deposit address retrieval, institution whitelist checks, wallet registration, and A-Token deposit, withdrawal, and transfer guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umy997](https://clawhub.ai/user/umy997)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent builders use Clevr Pay to check payment eligibility, obtain deposit information, register wallet mappings, and coordinate ClevrPay A-Token deposit, withdrawal, and transfer flows for verified counterparties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet registration, deposit-address retrieval, withdrawals, and token transfers can affect funds or expose irreversible transaction risk.

Mitigation: Require explicit confirmation and verify chain, token, amount, recipient, fees, and reversibility before proceeding.

Risk: Skipping A-Pass authentication in production can bypass an intended eligibility check.

Mitigation: Avoid using --skip-auth in production and complete A-Pass authentication before deposit workflows.

Risk: An exposed RPC URL in the evidence should be treated as credential-like material.

Mitigation: Redact or rotate sensitive RPC URLs before distribution.

## Reference(s):

- [Access Core Contract ABI](references/access_core.md)
- [Clevr Pay Skills API Documentation](references/api-doc.md)
- [Glossary and Retrieval Language](references/glossary.md)
- [Quick API Map](references/quick-api-map.md)
- [Retrieval and Boundaries](references/retrieval-and-boundaries.md)
- [Use Cases](references/use-cases.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline commands and API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation for wallet registration, deposit-address retrieval, withdrawals, and token transfers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
