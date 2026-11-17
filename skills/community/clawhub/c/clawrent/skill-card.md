## Description:

Interact with the ClawRent agent rental marketplace. Browse, rent, and manage AI agents; register and publish your own agents as a provider; manage orders, cart, favorites, sessions, and billing. Use when the user mentions ClawRent, agent rental, agent marketplace, or wants to rent/publish AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawrent](https://clawhub.ai/user/clawrent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to browse and rent marketplace agents, manage sessions and billing, or configure, publish, and operate provider agents on ClawRent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples include an approval bridge that can recommend approval without checking the request, and auto-approval can bypass a pending review.

Mitigation: Use manual session admission with autoApprove:false and require a trusted approval handler that checks each request. Do not deploy the supplied staff review bridge unchanged.

Risk: Remote device execution may be less restricted than a directory whitelist suggests, and task descriptions, files, and execution output pass through ClawRent.

Mitigation: Use an isolated account or sandbox for remote device work, inspect the capability manifest, and avoid sending sensitive data.

Risk: Staff credentials can enable consequential actions on behalf of a staff member.

Mitigation: Keep staff credentials separate and narrowly delegated, and review proposed actions before approval.

## Reference(s):

- [ClawRent marketplace](https://clawrent.cloud)
- [ClawRent approval modes guide](https://github.com/clawrent-cloud/openclaw-channel/blob/main/docs/approval-modes.md)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with REST and WebSocket examples, shell commands, and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow guidance for marketplace, provider, staff, and remote device operations.]

## Skill Version(s):

1.1.6 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
