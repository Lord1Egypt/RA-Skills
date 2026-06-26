## Description: <br>
Opinionated guide for building dApps on Arbitrum using Stylus (Rust) and/or Solidity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hummusonrails](https://clawhub.ai/user/hummusonrails) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold, build, test, deploy, and integrate Arbitrum dApps that use Stylus Rust contracts, Solidity contracts, local Nitro devnode workflows, and React frontends with viem or wagmi. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote one-line installation can execute installer behavior before the user reviews it. <br>
Mitigation: Prefer installing through ClawHub or cloning and reviewing the repository before running install.sh. <br>
Risk: The installer sends an install-count analytics ping unless disabled. <br>
Mitigation: Set ARBITRUM_SKILL_NO_ANALYTICS=1 before running install.sh to opt out. <br>
Risk: Deployment examples can perform real blockchain transactions, including mainnet or --broadcast operations. <br>
Mitigation: Use separate low-balance deployer wallets, keep private keys out of shell history where possible, and double-check the target network before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hummusonrails/arbitrum-dapp-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/hummusonrails) <br>
- [Stylus Rust Contracts](references/stylus-rust-contracts.md) <br>
- [Solidity Contracts](references/solidity-contracts.md) <br>
- [Frontend Integration](references/frontend-integration.md) <br>
- [Local Devnode Setup](references/local-devnode.md) <br>
- [Deployment](references/deployment.md) <br>
- [Testing](references/testing.md) <br>
- [Arbitrum Stylus Quickstart](https://docs.arbitrum.io/stylus/quickstart) <br>
- [Stylus SDK](https://github.com/OffchainLabs/stylus-sdk-rs) <br>
- [Nitro Devnode](https://github.com/OffchainLabs/nitro-devnode) <br>
- [viem](https://viem.sh) <br>
- [wagmi](https://wagmi.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain deployment commands and frontend or contract code snippets for user review before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
