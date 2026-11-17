## Description:

Free EVM transaction safety triage for agents before signing txs; routes deep explain/simulate/token-risk checks to the paid ClawMart EVM Transaction Safety Toolkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiancoombs](https://clawhub.ai/user/sebastiancoombs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for a lightweight pre-signing review of EVM transactions, approvals, calldata, value, target addresses, and simulation posture before signing or routing a transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A pre-signing checklist can miss transaction risk and should not be treated as proof that a transaction is safe.

Mitigation: Verify chain, addresses, calldata, value, and approvals independently, and pause when fields are missing, ambiguous, or inconsistent.

Risk: Wallet secrets or credentials could be exposed if a user supplies them during transaction review.

Mitigation: Do not request, reveal, or store seed phrases, private keys, session keys, or raw wallet credentials.

Risk: The free preview does not perform live execution, simulation, or token-risk checks by itself.

Mitigation: Use it as triage only, and use live checks or the paid toolkit when token risk, state changes, or simulation results matter before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sebastiancoombs/skills/evm-transaction-safety-preview)
- [ClawMart EVM Transaction Safety Toolkit](https://www.shopclawmart.com/listings/evm-transaction-safety-toolkit-89902e40)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown checklist and concise safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checklist-only preview; does not sign, broadcast, or make network calls by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
