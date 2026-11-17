## Description:

Run the BTCD collateralization flow on PGP chain. Use when the user asks to run a BTCD loan, collateralization flow, create/take orders, lock BTC, submit proofs, claim BTCD tokens, or repay loans on the PGP network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contact-nbwfoundation](https://clawhub.ai/user/contact-nbwfoundation)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a sequential BTCD collateralization lifecycle on the PGP (Elastos) chain, including order creation, order taking, BTC collateral locking, proof submission, BTCD claiming, and explicit user-requested repayment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real private keys and mainnet funds, and scanner evidence reports weak secret and transaction-safety controls.

Mitigation: Review scripts before installation, use wallets funded with only the minimum necessary amount, and do not reuse high-value private keys in the .env file.

Risk: Scanner guidance flags reruns and setup resets as dangerous until state handling is fixed.

Mitigation: Inspect state/flow-state.json before every step, avoid shared or CI environments, and treat reruns as requiring manual review of existing state and transaction IDs.

Risk: Blockchain transaction destinations and amounts can move irreversible funds.

Mitigation: Confirm all transaction destinations, collateral amounts, fees, and repayment actions manually before approving prompts or signing transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/contact-nbwfoundation/skills/btcd-skill-beta)
- [PGP Gas Swap](https://swap.pgpgas.org)
- [PGP Chain Explorer](https://pgp.elastos.io/tx/<hash>)
- [Primary PGP RPC Endpoint](https://api.elastos.io/pg)
- [BTCD Arbitrators PGP Subgraph](https://graph.eadd.co/subgraphs/name/btcd-arbitrators-pgp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-by-step execution guidance for a bundled Node.js workflow that writes local flow state and submits blockchain transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
