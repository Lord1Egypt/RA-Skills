## Description: <br>
Run the BTCD collateralization flow on PGP chain for BTCD loans, order creation and taking, BTC collateral locking, BTC proof submission, BTCD token claims, and loan repayment on the PGP network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contact-nbwfoundation](https://clawhub.ai/user/contact-nbwfoundation) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a BTCD collateralization lifecycle on the PGP chain, including setup, order management, BTC collateral locking, proof submission, BTCD claiming, and repayment when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled scripts use EVM and BTC private keys and can broadcast irreversible wallet transactions. <br>
Mitigation: Use only dedicated, limited-balance wallets and review dependencies, private key handling, network settings, balances, contract addresses, and transaction details before execution. <br>
Risk: The collateralization flow is stateful; running steps out of order or without checking state can create unsafe transaction behavior. <br>
Mitigation: Review state/flow-state.json before each step, run steps sequentially, and rely on the existing BTC transaction resume behavior instead of starting a new lock step. <br>
Risk: The repay step closes the loan position and unlocks collateral, which may be premature for the user's intent. <br>
Mitigation: Run repayment only when the user explicitly requests it and after confirming the calculated repayment amount, token approval, and BTC repayment transaction. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/contact-nbwfoundation/btcd-skill-beta) <br>
- [Publisher profile](https://clawhub.ai/user/contact-nbwfoundation) <br>
- [PGP chain explorer](https://pgp.elastos.io/tx/<hash>) <br>
- [PGP gas swap](https://swap.pgpgas.org) <br>
- [BTCD arbitrators subgraph](https://graph.eadd.co/subgraphs/name/btcd-arbitrators-pgp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration values, and Node.js execution steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sequential operational guidance for a stateful wallet and transaction workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
