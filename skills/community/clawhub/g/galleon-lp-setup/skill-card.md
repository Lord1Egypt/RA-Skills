## Description:

Checks a chain connection and identifies the data and tools an agent still needs for a liquidity-pool task, without authorizing wallet actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to check read-only chain connectivity, inventory liquidity-pool tools, and report what is missing before analysis or planning. It does not select pools or grant transaction authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RPC URLs or optional service keys may contain credentials.

Mitigation: Configure them through a secret store; do not include URLs, keys, or authorization headers in reports.

Risk: A fresh chain read may be mistaken for wallet, protocol, or trade readiness.

Mitigation: Report each capability separately and require task-specific checks before planning or execution.

Risk: Optional providers can introduce fees, permissions, or custody changes.

Mitigation: Add a provider only after user selection and review of its current permissions, fees, custody effects, and version.

## Reference(s):

- [Galleon LP Setup on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-lp-setup)
- [Tool connection map](references/connections.md)
- [Official LP tools](references/official-tools.md)
- [VFAT access and readiness](references/vfat.md)
- [Ethereum JSON-RPC documentation](https://ethereum.org/developers/docs/apis/json-rpc/)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown readiness report with observed chain details, capability statuses, missing tools, and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unobserved values are marked unknown; excludes RPC URLs, credentials, and private keys.]

## Skill Version(s):

0.6.1 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
