## Description:

Helps ESPN Fantasy Football managers sign in, monitor league activity, evaluate decisions, and manage team lineups and roster moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdm0830](https://clawhub.ai/user/jdm0830)

### License/Terms of Use:

MIT-0

## Use Case:

Fantasy football managers use this skill with an agent to check their ESPN league, receive alerts, assess trades and waivers, and manage lineups or player moves with appropriate approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent account access can enable unintended roster, waiver, or trade actions.

Mitigation: Require explicit confirmation for every roster, waiver, and trade action before execution.

Risk: Stored cookies and browser profiles can expose the ESPN account if accessed by others.

Mitigation: Restrict access to saved credentials, cookies, and profiles; delete them when no longer needed.

Risk: The login flow logs one-time codes and starts a VNC display without authentication.

Mitigation: Remove code logging and require authenticated display access before entering real credentials.

Risk: Background monitoring may continue accessing the league after interactive use ends.

Mitigation: Leave the monitoring timer disabled unless ongoing access is intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jdm0830/skills/espn-fantasy)
- [ClawHub publisher profile](https://clawhub.ai/user/jdm0830)
- [ESPN Fantasy API reference](artifact/references/espn-fantasy-api.md)
- [Login flow reference](artifact/references/login-flow.md)
- [Team management strategy](artifact/references/strategy.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text]

**Output Format:** [Markdown guidance and league-event alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can also execute authorized lineup and roster changes through the ESPN Fantasy API.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
