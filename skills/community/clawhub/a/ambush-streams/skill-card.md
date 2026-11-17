## Description:

Manage a user's Ambush news streams through the Ambush Streams MCP server. Use when the user wants to create, list, inspect, rename, change, pause, resume, or delete a stream; review emitted news; or process and deliver every new event to an existing destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambush-ai](https://clawhub.ai/user/ambush-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and manage Ambush news-monitoring streams, review emitted events, and configure processing and delivery to destinations already set up in Ambush.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting and routing enable ongoing delivery of stream events to configured destinations.

Mitigation: Check the destination before routing and avoid including sensitive details in monitoring prompts.

Risk: Deleting a stream is permanent, and muting a route cancels pending deliveries.

Mitigation: Confirm the exact stream and requested action before deleting or muting; use pause when the intent is to stop future stream activity temporarily.

## Reference(s):

- [Ambush](https://ambush.ai)
- [Manage Ambush Streams on ClawHub](https://clawhub.ai/ambush-ai/skills/ambush-streams)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Natural-language summaries and Ambush stream settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports tool-returned stream IDs and statuses; delivery depends on configured destinations and does not guarantee a particular story or delivery time.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
