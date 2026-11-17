## Description:

Safely deploys Move contracts to Aptos networks (devnet, testnet, mainnet) with pre-deployment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute Aptos Move contract deployments across devnet, testnet, and mainnet with security, testing, funding, deployment, upgrade, and verification checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-confirmed mainnet deploy or upgrade commands can submit high-impact blockchain transactions without an interactive confirmation.

Mitigation: Require explicit human review of the network, account, object address, code diff, compatibility, gas cost, and transaction impact before any mainnet deploy or upgrade, especially when --assume-yes is present.

Risk: Incorrect network, profile, address, or upgrade target can publish or upgrade the wrong Aptos package.

Mitigation: Confirm the target network, profile, named address, object address, balance, and explorer transaction details before and after deployment.

## Reference(s):

- [Aptos CLI Publishing](https://aptos.dev/build/cli/working-with-move-contracts)
- [Aptos Network Endpoints](https://aptos.dev/nodes/networks)
- [Aptos Gas and Fees](https://aptos.dev/concepts/gas-txn-fee)
- [Aptos Testnet Faucet](https://aptos.dev/network/faucet?address=<your_address>)
- [Aptos Explorer](https://explorer.aptoslabs.com/?network=mainnet)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists and inline bash, Move, and deployment-record examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Aptos network selection, profile setup, funding, deployment, upgrade, verification, and documentation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
