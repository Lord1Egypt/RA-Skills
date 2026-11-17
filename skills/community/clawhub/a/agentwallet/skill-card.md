## Description:

Provides an agent wallet for EVM chain transactions, token transfers, swaps, smart contract interactions, and raw signing without exposing private keys to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to create and operate policy-controlled wallets for EVM transfers, swaps, contract calls, and signing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants high-impact transaction and signing authority.

Mitigation: Use it only when the operator accepts agent wallet capability, configure restrictive policies before funding the wallet, and require human approval for sensitive transactions.

Risk: A created wallet can operate before the human owner claims it and applies policies.

Mitigation: Share and claim the wallet URL immediately, avoid funding unclaimed wallets, and revoke or relink keys when control changes.

Risk: Arbitrary calldata and raw signing can create unintended financial or protocol effects.

Mitigation: Avoid arbitrary calldata and raw signing unless necessary, and review destination addresses, chain IDs, values, calldata, and approval status before execution.

Risk: Using a mutable npm CLI version can change runtime behavior.

Mitigation: Prefer a pinned and verified Vincent CLI version instead of @latest.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glitch003/skills/agentwallet)
- [Vincent homepage](https://heyvincent.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet creation, balance checks, transfers, swaps, transaction submission, relinking, and raw signing guidance.]

## Skill Version(s):

1.0.70 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
