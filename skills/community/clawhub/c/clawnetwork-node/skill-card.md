## Description:

Enables OpenClaw and other agents to use ClawNetwork blockchain capabilities, including running a lightweight node, earning CLAW as a miner, and managing balances, transfers, identity registration, faucet access, and service discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flute](https://clawhub.ai/user/flute)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to operate ClawNetwork blockchain capabilities through an agent, including checking node status and balances, transferring CLAW, registering identities or services, using a faucet, and discovering services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A CLAW transfer could be sent to the wrong recipient or for the wrong amount.

Mitigation: Require explicit user confirmation, show the full recipient address, validate 64-character hex addresses, and confirm the amount before executing transfers.

Risk: Agent identity or service registration may publish information on-chain.

Mitigation: Confirm that the user intends to register the identity or service and review submitted names, endpoints, descriptions, and prices before registration.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown or plain text responses with plugin calls and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require explicit user confirmation before token transfers.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
