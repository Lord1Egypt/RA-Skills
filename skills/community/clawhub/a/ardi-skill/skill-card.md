## Description: <br>
Ardi Skill helps an agent solve multilingual riddles, submit Base mainnet commit-reveal transactions, and mint or manage Ardinal NFTs for the Ardi WorkNet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyangxing](https://clawhub.ai/user/yangyangxing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and operators use this skill to run the Ardi WorkNet flow: check wallet and stake readiness, reason over riddle epochs, commit and reveal answers, mint winning Ardinal NFTs, and manage related rewards or transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize wallet-backed transactions, purchases, staking, marketplace operations, reward claims, and NFT transfers on Base mainnet. <br>
Mitigation: Use a dedicated low-balance wallet, review quoted costs before execution, and require explicit operator confirmation before spend, claim, list, buy, stake, or transfer commands. <br>
Risk: Autonomous mining can create recurring LLM usage, gas spending, and unattended commit, reveal, or inscribe attempts. <br>
Mitigation: Enable auto-mine only when the operator accepts unattended operation; monitor status output and stop the timer or loop when spending limits or operational goals are reached. <br>
Risk: Installer scripts fetch executable releases and can change what is installed over time. <br>
Mitigation: Inspect installers and release artifacts before running them, or pin a reviewed release instead of installing the latest version blindly. <br>
Risk: Deleting or losing the local state file between commit and reveal can make the answer nonce unavailable and forfeit the commit bond. <br>
Mitigation: Preserve and back up the per-address state file before migration or cleanup, and avoid deleting Ardi state while commits are pending. <br>
Risk: The wallet integration does not use a session-token model and may leave approvals or spending authority active after use. <br>
Mitigation: Keep wallet funds limited, review token and NFT approvals after operation, and revoke unnecessary approvals. <br>


## Reference(s): <br>
- [ClawHub Ardi Skill release](https://clawhub.ai/yangyangxing/ardi-skill) <br>
- [Ardi Skill homepage](https://github.com/awp-worknet/ardi-skill) <br>
- [AWP Wallet dependency](https://github.com/awp-core/awp-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires terminal access, awp-wallet, Base mainnet funds, and preservation of local Ardi state between commit and reveal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
