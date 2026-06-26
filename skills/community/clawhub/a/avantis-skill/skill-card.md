## Description: <br>
Execute leverage trading on Avantis (Base). Long/short crypto, forex, commodities with up to 100x leverage. Uses Python SDK with direct wallet integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droppingbeans](https://clawhub.ai/user/droppingbeans) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and trading agents use this skill to inspect, open, and close leveraged Avantis positions on Base using wallet-signed Python SDK commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a wallet signer and submit real Avantis/Base mainnet transactions, which can put funds at risk. <br>
Mitigation: Use only a dedicated, low-funded wallet and require manual review of approvals, collateral, leverage, take-profit, stop-loss, and close-position details before broadcasting. <br>
Risk: Plaintext or exposed private keys could allow unauthorized wallet use. <br>
Mitigation: Do not use a primary wallet, avoid plaintext private-key files, and rotate any exposed test keys before installing or running the skill. <br>
Risk: Leveraged trading can rapidly liquidate collateral or generate losses and fees. <br>
Mitigation: Start with small collateral, use stop losses, monitor positions, and do not risk funds the user cannot afford to lose. <br>


## Reference(s): <br>
- [Avantis Quick Start](references/quick-start.md) <br>
- [ClawHub skill page](https://clawhub.ai/droppingbeans/avantis-skill) <br>
- [Avantis platform](https://avantisfi.com) <br>
- [Avantis SDK docs](https://sdk.avantisfi.com) <br>
- [Avantis trading guide](https://docs.avantisfi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that query balances, approve USDC, and submit wallet-signed Base mainnet transactions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
