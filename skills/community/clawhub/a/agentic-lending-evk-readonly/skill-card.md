## Description: <br>
Read-only EVK-first agentic lending workflow planning and verification for Api3-backed markets, covering oracle route resolution, feed readiness, funding classification, EVK artifact preparation, deployability assessment, and post-deploy borrow-proof planning without transaction submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daav3](https://clawhub.ai/user/daav3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and review EVK lending-market workflows that depend on Api3 feeds. It helps inspect route readiness, funding classification, deployment artifacts, blockers, and borrow-proof planning while staying in read-only or dry-run mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers high-impact crypto lending workflows where following generated commands or plans without review could affect real wallets or markets. <br>
Mitigation: Use it only as a read-only planning aid; do not run live or broadcast commands from the skill output. <br>
Risk: Wallet addresses, signer configuration, RPC endpoints, and borrow-proof configs can expose sensitive operational details or lead to signer-backed execution if reused carelessly. <br>
Mitigation: Do not provide private keys or real signer secrets, keep runtime configs outside git, and review any local scripts separately before wallet, borrow, swap, funding, or deployment use. <br>
Risk: Deployment readiness can be mistaken for proven borrowability. <br>
Mitigation: Treat deployment success and borrowability proof as separate milestones, and use this skill only to plan proof inputs and blockers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daav3/agentic-lending-evk-readonly) <br>
- [Agentic Lending EVK workflow reference](references/api_reference.md) <br>
- [Current capabilities and limits](references/current_capabilities.md) <br>
- [EVK borrow-proof planning checklist](references/live-borrow-checklist.md) <br>
- [Arbitrum eUSDC-1 isolated example](references/arbitrum-eusdc1-isolated-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only planning output; live funding, deployment, transaction submission, and live borrow proof are out of scope.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
