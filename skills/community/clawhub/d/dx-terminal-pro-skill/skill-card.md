## Description:

Manage a DX Terminal Pro trading agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[octal-crypto](https://clawhub.ai/user/octal-crypto)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect and influence a DX Terminal Pro trading agent, including portfolio state, strategies, market data, swaps, and vault deposits or withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wallet private key can control real funds and is used by shell commands in the skill.

Mitigation: Use the skill only in a trusted environment, avoid exposing raw private keys in shell history or process lists, and never share DX_TERMINAL_PRIVATE_KEY.

Risk: Write actions can change trading settings, alter strategies, or deposit and withdraw ETH.

Mitigation: Before execution, independently verify the vault address and contract, inspect values and parameters, simulate the transaction, and require explicit human approval.

## Reference(s):

- [DX Terminal](https://terminal.markets)
- [ClawHub Skill Page](https://clawhub.ai/octal-crypto/skills/dx-terminal-pro-skill)
- [Publisher Profile](https://clawhub.ai/user/octal-crypto)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cast, curl, jq, and DX_TERMINAL_PRIVATE_KEY for wallet-authenticated actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
