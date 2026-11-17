## Description:

Borrow from Aave via credit delegation. Agent self-funds by borrowing against delegator collateral. Supports borrow, repay, health checks. Works on Aave V2/V3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronjmars](https://clawhub.ai/user/aaronjmars)

### License/Terms of Use:


## Use Case:

Developers and external agent operators use this skill to let an agent check Aave delegation status, borrow delegated assets, and repay debt using shell-based workflows. It is intended for controlled agent wallets where a delegator has supplied collateral and explicitly approved per-asset credit delegation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent live Aave borrowing authority against delegated collateral.

Mitigation: Use a dedicated low-value agent wallet, delegate only small per-asset allowances, cap each transaction, and revoke delegation when the agent is idle.

Risk: The security summary reports plaintext wallet-key handling for the agent wallet.

Mitigation: Avoid plaintext private keys where possible, keep file permissions restrictive, never store the delegator private key, and keep only minimal gas in the agent wallet.

Risk: Built-in health-factor and transaction-cap checks are not complete protection against liquidation or misuse.

Mitigation: Review each deployment carefully, monitor health factor externally, keep conservative health-factor thresholds, and test with small limits before allowing real funds.

## Reference(s):

- [ClawHub Agent Credit Skill Page](https://clawhub.ai/aaronjmars/skills/agent-credit)
- [Aave V3 Docs](https://docs.aave.com/developers)
- [Aave Credit Delegation Guide](https://docs.aave.com/developers/guides/credit-delegation)
- [Aave DebtToken Reference](https://docs.aave.com/developers/tokens/debttoken)
- [Aave Address Book](https://github.com/bgd-labs/aave-address-book)
- [Foundry Book](https://book.getfoundry.sh/)
- [Artifact README](artifact/README.md)
- [Artifact Safety Guidelines](artifact/safety.md)
- [Artifact Deployment Addresses](artifact/deployments.md)
- [Artifact Contract Addresses](artifact/contracts.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, json]

**Output Format:** [Markdown guidance with bash commands, JSON configuration, and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included scripts can read Aave status and submit borrow, repay, and approval transactions from a configured agent wallet.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
