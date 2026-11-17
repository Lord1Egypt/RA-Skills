## Description:

Use when you need to operate the @metamask/gator-cli to initialize profiles, upgrade EOA to EIP-7702, grant, redeem, and revoke ERC-7710 delegations, or inspect balances and delegations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayushbherwani1998](https://clawhub.ai/user/ayushbherwani1998)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate the Gator CLI for MetaMask smart account delegation workflows, including profile initialization, account upgrade, grant creation, redemption, revocation, balance checks, and delegation inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides high-impact blockchain account actions such as signing delegations, redeeming transfers, revoking delegations, and upgrading accounts.

Mitigation: Use low-value test accounts and verify profile, chain, recipient addresses, contract targets, amounts, call data, and delegation scopes before signing.

Risk: Gator CLI profiles may store private keys in plaintext JSON.

Mitigation: Do not use accounts with significant funds, and protect or remove local profile files after testing.

Risk: The installation guidance uses an unpinned global npm package.

Mitigation: Review or pin the npm package version before global installation.

## Reference(s):

- [MetaMask Smart Accounts Kit documentation](https://docs.metamask.io/smart-accounts-kit)
- [Gator CLI skill page](https://clawhub.ai/ayushbherwani1998/skills/gator-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should preserve user-supplied chain, profile, address, amount, call data, and delegation scope values.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
