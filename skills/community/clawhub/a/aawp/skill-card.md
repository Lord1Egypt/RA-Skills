## Description: <br>
AAWP (AI Agent Wallet Protocol) gives AI agents wallet lifecycle management, token transfers, DEX swaps, cross-chain bridging, arbitrary EVM contract interactions, DCA automation, and price alerts through an installer package that provisions the runtime separately. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wfce](https://clawhub.ai/user/wfce) <br>

### License/Terms of Use: <br>
BUSL-1.1 <br>


## Use Case: <br>
External developers and agent operators use this skill to let an AI agent provision and operate an EVM-compatible wallet, inspect balances, execute transfers or swaps, and configure scheduled wallet activity. It is intended for agents that need autonomous on-chain wallet workflows with human approval for provisioning and higher-risk setup actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over wallet funds and autonomous on-chain transactions. <br>
Mitigation: Start with test funds, pin the expected wallet address, define spend limits, and keep a clear pause or recovery procedure before enabling live operations. <br>
Risk: The package is installer-only and fetches the higher-risk runtime code, including the native signing component, after installation. <br>
Mitigation: Review the runtime that will actually be provisioned, verify native binary provenance and factory approval independently, and avoid treating the package files alone as sufficient review. <br>
Risk: Wallet provisioning and daemon operation involve private key material and an encrypted agent signing seed. <br>
Mitigation: Keep keys and generated config out of shell history, logs, and source control; protect local config directories; and use human approval for first-time provisioning. <br>
Risk: Cron strategies, auto-swaps, arbitrary contract calls, token approvals, NFT transfers, and DeFi borrowing can create recurring or hard-to-reverse financial exposure. <br>
Mitigation: Enable those actions only after human review, small-value testing, and confirmation that transaction limits and monitoring are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wfce/aawp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wfce) <br>
- [AAWP homepage](https://aawp.ai) <br>
- [AAWP package-declared repository](https://github.com/aawp-ai/aawp.git) <br>
- [BaseScan factory contract](https://basescan.org/address/0xAAAA3Df87F112c743BbC57c4de1700C72eB7aaAA) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides wallet setup, daemon management, wallet operations, and scheduled EVM workflows.] <br>

## Skill Version(s): <br>
1.6.8 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
