## Description:

Scaffold and fetch event logs from EVM smart contracts via RPC, ABI discovery or user-provided ABI, event selection, log pulling, and ABI-based parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkkchen](https://clawhub.ai/user/lkkchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold a local Node.js project, configure an EVM chain and contract address, retrieve or provide an ABI, choose contract events, and produce raw plus parsed event logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RPC URLs, command-line API keys, private-chain addresses, or proprietary ABIs may be exposed because the skill stores configuration and ABI files in the generated project and calls user-provided endpoints.

Mitigation: Use a dedicated public HTTPS RPC endpoint without embedded secrets, avoid passing API keys on the command line, and avoid private-chain addresses or proprietary ABIs unless local project storage is acceptable.

Risk: Project initialization runs a Node package install and downloads dependencies before the log workflow can run.

Mitigation: Review the generated package versions and dependency list before installation, and run the project in an isolated workspace when evaluating unfamiliar releases.

Risk: ABI discovery and log retrieval make network calls to Sourcify, Etherscan-compatible APIs, and configured RPC providers.

Mitigation: Confirm that outbound network access to these services and RPC endpoints is acceptable before running the fetch and pull commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkkchen/skills/fetch-evm-logs)
- [Reference](reference.md)
- [Examples](examples.md)
- [Sourcify ABI API](https://sourcify.dev/server/v2/contract/${chainId}/${address}?fields=abi)
- [Etherscan API v2](https://api.etherscan.io/v2/api?chainid=${chainId})

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Text, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated project files; runtime output is newline-delimited raw log text plus parsed JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces output/{address}_{chainId}/logs.txt and output/{address}_{chainId}/logs.json after pnpm s1 and pnpm s2.]

## Skill Version(s):

1.0.0 (source: server release metadata and template package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
