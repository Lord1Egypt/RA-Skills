## Description:

An opinionated guide for building Arbitrum dApps with Stylus Rust, Solidity, local devnode workflows, deployment guidance, and React frontend integration with viem and wagmi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hummusonrails](https://clawhub.ai/user/hummusonrails)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scaffold, write, test, deploy, and integrate Arbitrum dApps using Stylus Rust contracts, Solidity contracts, Foundry, nitro-devnode, viem, and wagmi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start installer runs a mutable remote shell script and the installer updates from the main branch.

Mitigation: Review the installer before running it, prefer cloning a pinned tag or commit manually, and avoid automatic updates from a mutable branch.

Risk: The installer sends an opt-out GoatCounter install-count request.

Mitigation: Set ARBITRUM_SKILL_NO_ANALYTICS=1 before installation if install telemetry is not desired.

Risk: Deployment examples can spend real funds or expose secrets if production keys are placed directly on command lines.

Mitigation: Use throwaway local keys for devnodes, avoid putting real private keys directly on command lines, simulate before --broadcast, and treat Arbitrum One as real mainnet.

## Reference(s):

- [Stylus Rust Contracts](references/stylus-rust-contracts.md)
- [Solidity Contracts on Arbitrum](references/solidity-contracts.md)
- [Frontend Integration](references/frontend-integration.md)
- [Local Devnode Setup](references/local-devnode.md)
- [Deployment](references/deployment.md)
- [Testing](references/testing.md)
- [Arbitrum Stylus Quickstart](https://docs.arbitrum.io/stylus/quickstart)
- [Stylus SDK](https://github.com/OffchainLabs/stylus-sdk-rs)
- [Nitro Devnode](https://github.com/OffchainLabs/nitro-devnode)
- [viem](https://viem.sh)
- [wagmi](https://wagmi.sh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks, command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include smart contract snippets, frontend integration snippets, deployment commands, environment variable guidance, and testing checklists.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
