## Description:

Enforce fine-grained spending policies before executing any payment, transfer, swap, or bridge. Checks Conto policy engine for approval before money leaves your wallet. Use /conto to manage policies or check payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwattana](https://clawhub.ai/user/kwattana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to make an OpenClaw agent check Conto spending policies before payments, transfers, swaps, bridges, and x402 API payments. It also supports reviewing pending approvals and managing policies when the configured SDK key permits administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can participate in payment enforcement and, depending on wallet mode, payment execution.

Mitigation: Use it only for agents that should handle payments, restrict wallet spend limits, and require explicit confirmation before sending funds.

Risk: Admin SDK keys allow policy creation, updates, deletion, and broader wallet or agent management actions.

Mitigation: Prefer a Standard SDK key for routine payment checks and approvals; use an Admin key only when policy administration is required.

Risk: Weak control boundaries can allow bypass if wallet signing is not gated on policy approval.

Mitigation: Gate wallet signing or credentials on Conto approval, verify approved amount, recipient, and chain before execution, and fail closed when the Conto API is unavailable.

Risk: The SDK key is stored in the local OpenClaw configuration.

Mitigation: Review file permissions on ~/.openclaw/openclaw.json and limit access to the configured agent account.

## Reference(s):

- [ClawHub: Conto Skill](https://clawhub.ai/kwattana/skills/conto)
- [Conto Homepage](https://conto.finance)
- [Conto SDK Documentation](https://conto.finance/docs)
- [Policy Documentation](https://conto.finance/docs/policies)
- [Buyer-Side Control](https://conto.finance/docs/guides/buyer-side-control)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, network access to the Conto API, and a CONTO_SDK_KEY for runtime commands.]

## Skill Version(s):

1.10.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
