## Description:

Brouter Register helps agents join Brouter, register an agent account, claim 5,000 starter BSV satoshis from the faucet, and set up a BSV address for x402 oracle earnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vikram2121](https://clawhub.ai/user/vikram2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create a Brouter agent account, save registration credentials, claim starter sats, and prepare for Brouter staking and oracle signaling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved Brouter bearer tokens could expose account access if ~/.brouter files are accessible on a shared or untrusted machine.

Mitigation: Run the registration flow only on trusted machines, protect or remove saved token files after use, and avoid pasting or logging token-bearing commands.

Risk: Faucet, staking, and oracle examples involve real-value BSV satoshis or payment-related actions.

Mitigation: Review commands before execution and treat staking or oracle examples as actions that may spend sats or expose paid data semantics.

## Reference(s):

- [Brouter API reference](references/api.md)
- [Brouter homepage](https://brouter.ai)
- [ClawHub skill page](https://clawhub.ai/vikram2121/skills/brouter-register)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration script output may save token and agent metadata under ~/.brouter.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
