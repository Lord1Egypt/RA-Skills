## Description:

Register ENS names, create subdomains, and publish IPFS sites without manual contract calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeugh-eth](https://clawhub.ai/user/zeugh-eth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check ENS name status, register .eth names, create subdomains, and publish IPFS content through command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet credentials may be exposed or mishandled during ENS operations.

Mitigation: Use a dedicated low-value wallet, prefer keystore or environment-variable inputs, and avoid raw private keys or command-line passwords.

Risk: ENS registration and subdomain changes can submit irreversible Ethereum mainnet transactions.

Mitigation: Run read-only or dry-run checks first, verify names, costs, addresses, and transaction details manually, and keep enough ETH only for the intended operation.

Risk: Installer commands or copied setup commands may execute privileged system changes.

Mitigation: Independently inspect installer commands before execution and avoid running curl-to-sudo style commands without verification.

## Reference(s):

- [ENS Basics](references/ens-basics.md)
- [ENS Documentation](https://docs.ens.domains)
- [Dependency Guide](DEPENDENCIES.md)
- [Quick Start](QUICK-START.md)
- [Cost Guide](COSTS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents through Node.js scripts that inspect ENS state and submit Ethereum mainnet transactions.]

## Skill Version(s):

1.2.0 (source: release evidence, frontmatter, CHANGELOG; scripts/package.json differs: 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
