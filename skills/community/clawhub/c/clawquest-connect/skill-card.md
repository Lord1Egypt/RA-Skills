## Description:

Connects Claw Quest Android to an OpenClaw gateway using a manual WebSocket URL and token/password flow, with optional WhatsApp handoff and one-time matching device approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandrokitchener](https://clawhub.ai/user/sandrokitchener)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to pair Claw Quest Android with their OpenClaw gateway by sending the current gateway URL and token or password, then approving one matching Android pairing request when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may place a reusable gateway token or password into WhatsApp or chat history.

Mitigation: Confirm the destination before sharing credentials and prefer short-lived pairing codes when available.

Risk: The skill may automatically approve a device with operator-level write access.

Mitigation: Review the exact pending device request before approval and approve only a Claw Quest Android request with the expected role and scopes.

## Reference(s):

- [Claw Quest Connect on ClawHub](https://clawhub.ai/sandrokitchener/skills/clawquest-connect)
- [sandrokitchener ClawHub profile](https://clawhub.ai/user/sandrokitchener)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and concise connection details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the gateway URL and the current token or password needed for manual setup.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
