## Description:

Cannon helps AI agents build, test, deploy, inspect, publish, and troubleshoot Cannon packages for Ethereum smart contract deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbeal-eth](https://clawhub.ai/user/dbeal-eth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an AI assistant generate or review Cannon CLI commands, cannonfile TOML, deployment workflows, testing patterns, registry publishing steps, and troubleshooting guidance for Ethereum smart contract packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-network Cannon deployments, registry registration, publisher management, and package publishing can be irreversible.

Mitigation: Use local testing and dry-run mode first, explain the planned operation, require explicit approval before funded or production network actions, and double-check chain ID, package name, version, and preset.

Risk: Cannon workflows may involve funded wallets or private keys.

Mitigation: Prefer hardware or managed signers, avoid raw private keys where possible, keep any required key material scoped to the environment, and run the skill in an isolated development workspace.

Risk: Tool installation and package publishing steps can pull remote code or expose project contents through registry and IPFS workflows.

Mitigation: Pin and verify tooling before use, review package contents before publishing, and use Cannon privacy controls when source code should not be included in published packages.

## Reference(s):

- [CLI Reference](references/cli.md)
- [Cannonfile Specification](references/cannonfile.md)
- [Testing Patterns](references/testing.md)
- [Registry and Publishing](references/registry.md)
- [Cannon JSON Schema](https://raw.githubusercontent.com/usecannon/cannon/refs/heads/dev/packages/lsp/src/schema.json)
- [Cannon Fragment Schema](https://raw.githubusercontent.com/usecannon/cannon/refs/heads/dev/packages/lsp/src/schema-fragment.json)
- [Cannon Deploy](https://usecannon.com/deploy)
- [Cannon Website](https://usecannon.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, TOML snippets, and Solidity examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes safety guidance for dry-runs, wallet and key handling, chain selection, testing, and registry publishing.]

## Skill Version(s):

2.26.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
