## Description:

Creates a private Discord support ticket channel request for a user who needs manual help with unresolved or privacy-sensitive issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpd](https://clawhub.ai/user/charles-lpd)

### License/Terms of Use:

MIT-0

## Use Case:

External support agents and Discord server operators use this skill to request a private ticket channel when a user's issue cannot be resolved automatically or requires sensitive troubleshooting details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may report that a private Discord channel was created before channel creation and permission overwrites are verified.

Mitigation: Use only with a trusted OpenClaw Discord adapter that verifies channel creation and permission overwrites before telling the user the channel is private or asking for sensitive details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charles-lpd/skills/create-ticket)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [JSON string containing a channel-creation action, payload, and user-facing message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires username and userId; optional issue defaults to General Support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
