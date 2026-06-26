## Description: <br>
Automates Ceaser Protocol ETH shield and unshield transfers on Base L2 by generating a temporary hot wallet, guiding funding, signing and broadcasting transactions, and refunding remaining ETH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zyra-V21](https://clawhub.ai/user/Zyra-V21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to perform a high-automation ETH transfer through the Ceaser privacy workflow on Base L2. It is intended for users who explicitly want automated signing and understand that the agent handles temporary wallet secrets and irreversible transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent handles temporary wallet secrets and can broadcast irreversible on-chain transactions. <br>
Mitigation: Use small amounts, save the mnemonic and backup string offline, and confirm recipient and refund addresses before funding. <br>
Risk: Automated signing creates observable links between the funding wallet, hot wallet, shield transaction, and refund. <br>
Mitigation: Use this skill only when automated signing is required and prefer a manual signing workflow when stronger privacy is needed. <br>
Risk: The workflow depends on the Ceaser package, facilitator, contract address, and Base RPC availability. <br>
Mitigation: Verify the package version, contract address, facilitator status, denomination, and fees before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zyra-V21/ceaser-send) <br>
- [Ceaser homepage](https://ceaser.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface transaction hashes, temporary wallet recovery material, and status messages during execution.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
