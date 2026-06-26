## Description: <br>
Self-custodial Bitcoin and Lightning wallet for AI agents that can help send and receive sats via Lightning Network, Spark, or on-chain Bitcoin when configured with BreezClaw and a Breez API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robertclarkson](https://clawhub.ai/user/robertclarkson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent check wallet status and balance, generate receive requests, review fee estimates, and prepare Bitcoin, Lightning, or Spark payments. It is intended for wallet operations that require careful human confirmation before funds move. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority over a self-custodial Bitcoin wallet and real funds. <br>
Mitigation: Start with testnet or a low-balance wallet and manually verify the recipient, amount, network, and fee before approving any send. <br>
Risk: The installation flow depends on mutable third-party wallet code. <br>
Mitigation: Review or pin the external BreezClaw repository before running npm install. <br>
Risk: Wallet recovery data can be exposed if the mnemonic is requested or shared in chat. <br>
Mitigation: Avoid exposing the mnemonic in chat and restrict mnemonic retrieval to explicit, intentional recovery workflows. <br>


## Reference(s): <br>
- [BreezClaw repository](https://github.com/onesandzeros-nz/BreezClaw) <br>
- [Breez SDK](https://breez.technology/sdk/) <br>
- [ClawHub skill page](https://clawhub.ai/robertclarkson/bitcoin-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing wallet guidance that includes installation, configuration, wallet tool usage, fee review, and explicit confirmation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
