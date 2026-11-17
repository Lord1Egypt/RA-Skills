## Description:

Helps an agent place and manage US phone calls, handle call handoffs, and configure ClawCall calling preferences and inbound answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawcall-dev](https://clawhub.ai/user/clawcall-dev)

### License/Terms of Use:

MIT-0

## Use Case:

People and their agents use ClawCall to contact US businesses, navigate phone menus, arrange appointments, and manage inbound calls and calling preferences. Live handoff lets the user take over sensitive exchanges.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Real phone calls and paid features may incur charges or make commitments on the user's behalf.

Mitigation: Confirm the requested task and decision limits, and explain relevant costs before acting.

Risk: Calls, recordings, and live handoffs may expose sensitive information.

Mitigation: Do not solicit or relay restricted information; hand off sensitive steps to the user and do not claim recording or transcription stops.

Risk: Credentials or customer details could be exposed when using hosted API instructions.

Mitigation: Keep credentials confidential, send them only to the ClawCall API, and fetch public guides without credentials or customer details.

## Reference(s):

- [ClawCall skill on ClawHub](https://clawhub.ai/clawcall-dev/skills/clawcall-dev)
- [ClawCall](https://clawcall.dev)
- [ClawCall API guides](https://api.clawcall.dev/guides/v1/index.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can initiate real US phone calls through ClawCall with user authorization.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
