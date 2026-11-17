## Description:

Eth Labels helps agents look up labeled crypto addresses, token metadata, and balances across major EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawsbot](https://clawhub.ai/user/dawsbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and crypto analysts use this skill to identify labeled EVM addresses, search known entities, retrieve token metadata, and check balances during wallet, transaction, or protocol research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup relies on mutable external GitHub and npm code that was not included in the reviewed artifact.

Mitigation: Review the upstream repository before installing, pin it to a known commit or release, prefer locked dependencies and local binaries over unpinned npx, and run the MCP server with only the permissions and environment variables it needs.

Risk: Balance checks can use custom RPC endpoints, which may expose queried addresses or depend on an untrusted endpoint.

Mitigation: Use trusted RPC endpoints and avoid sending sensitive investigation targets to infrastructure you do not control or trust.

## Reference(s):

- [Eth Labels ClawHub Page](https://clawhub.ai/dawsbot/skills/eth-labels)
- [Eth Labels Swagger Docs](https://eth-labels.com/swagger)
- [Eth Labels Labeled Accounts](https://eth-labels.com/accounts)
- [Eth Labels Repository](https://github.com/dawsbot/eth-labels)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool calls, JSON configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP results may include address labels, token metadata, chain identifiers, and formatted ETH balances.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
