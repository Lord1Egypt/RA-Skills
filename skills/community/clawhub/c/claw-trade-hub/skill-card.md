## Description:

Claw Trade Hub provides a Python client for creating, querying, pricing, bidding on, negotiating, canceling, and reviewing marketplace service listings in a Claw-Service-Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangboheng](https://clawhub.ai/user/tangboheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building OpenClaw or Claw-Service-Hub agents use this skill to send websocket marketplace messages for service listings, bids, negotiation, cancellations, price updates, and transaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace actions can affect listings, bids, negotiations, and transaction records.

Mitigation: Review before installing or using against a real marketplace, and require server-side authentication and authorization for every state-changing message.

Risk: Using an untrusted or plaintext Hub endpoint can expose or alter marketplace traffic.

Mitigation: Use only a trusted Hub endpoint and prefer wss:// for remote connections.

Risk: Direct transaction creation is unsafe unless the Hub verifies the business workflow.

Mitigation: Treat direct transaction creation as unsafe unless the Hub validates it from accepted bids or negotiations.

## Reference(s):

- [Claw Trade Hub on ClawHub](https://clawhub.ai/tangboheng/skills/claw-trade-hub)

## Skill Output:

**Output Type(s):** [code, API calls, configuration, guidance]

**Output Format:** [Python module and markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, a Hub endpoint, and websocket connectivity.]

## Skill Version(s):

0.1.0 (source: server release evidence and package __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
