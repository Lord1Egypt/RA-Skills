## Description:

Interact with the Cavos CLI for Starknet wallet operations, including transfers, approvals, contract calls, session management, and transaction monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adrianvrj](https://clawhub.ai/user/adrianvrj)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate Cavos CLI workflows for Starknet wallet status, session import, token transfers, approvals, contract calls, multicalls, simulation, and transaction monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned third-party CLI for wallet sessions and on-chain operations.

Mitigation: Use only a trusted, pinned, audited Cavos CLI version before installing or running commands.

Risk: Session tokens and transaction-changing commands can affect wallet security or assets.

Mitigation: Avoid passing session tokens through untrusted runtime installs and require explicit confirmation of network, token, amount, recipient, spender, contract, entrypoint, and calldata before any transaction-changing command.

## Reference(s):

- [Cavos Dashboard](https://agent.cavos.xyz/)
- [ClawHub skill listing](https://clawhub.ai/adrianvrj/skills/cavos-cli-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and recommends Cavos CLI JSON output where available.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
