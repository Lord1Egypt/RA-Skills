## Description:

Deliver real-time websocket updates for intent, quote, negotiation, order, and payment events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add websocket push channels, subscription authorization, event replay, and connection lifecycle handling for market clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence describes this as implementation guidance rather than a complete runtime package.

Mitigation: Verify referenced runtime files and tests separately before relying on the implementation in production.

Risk: Unauthorized websocket subscriptions could expose market events to the wrong client or role.

Mitigation: Validate channel permissions for every subscription and return structured errors for unauthorized attempts.

Risk: Unbounded websocket queues can cause memory growth during slow-client or reconnect scenarios.

Mitigation: Enforce per-connection queue limits, heartbeat-based cleanup, and replay retention windows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with code-oriented contracts and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on websocket event contracts, channel authorization, replay cursors, and lifecycle guardrails.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
