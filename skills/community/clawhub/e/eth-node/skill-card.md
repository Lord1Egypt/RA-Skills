## Description:

Manage Ethereum execution client nodes: start, stop, check sync status, inspect peers, review logs, and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apexfork](https://clawhub.ai/user/apexfork)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage local Ethereum execution client nodes, including reth and geth, and to inspect sync, peers, logs, and JSON-RPC status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running untrusted Ethereum clients can expose the operator to compromised node software.

Mitigation: Install trusted clients and prefer pinned or verified releases, especially for reth.

Risk: Exposing JSON-RPC port 8545, admin APIs, or debug namespaces to a public network can allow unauthorized node control or sensitive diagnostics access.

Mitigation: Keep RPC and admin/debug namespaces bound to localhost and avoid public exposure of port 8545.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apexfork/skills/eth-node)
- [Publisher profile](https://clawhub.ai/user/apexfork)
- [Skill homepage](https://github.com/Fork-Development-Corp/openclaw-web3-skills/tree/master/eth-node)
- [reth source repository](https://github.com/paradigmxyz/reth)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash and JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume a local Ethereum execution client and localhost JSON-RPC endpoint.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
