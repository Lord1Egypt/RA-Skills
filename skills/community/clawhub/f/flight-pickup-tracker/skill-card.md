## Description:

Track a flight in real-time and notify when to leave for airport pickup based on distance to destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundiraman](https://clawhub.ai/user/sundiraman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to coordinate airport pickups for a named flight by checking live flight position, estimating arrival timing, and producing leave-by guidance. It is not intended for general flight status, travel planning, or airport information requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because shipped files do not match the promised end-to-end pickup workflow.

Mitigation: Review the package before installing and verify that drive-time and leave-by calculations are present and working in the installed artifact.

Risk: API keys may be exposed when passed through command-line arguments or stored without care.

Mitigation: Use restricted API keys, avoid command-line key arguments when possible, and prefer environment or secret-management mechanisms with limited scope.

Risk: Pickup monitoring can use sensitive location details and scheduled background checks.

Mitigation: Confirm the pickup address explicitly and keep scheduled checks visible and cancellable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sundiraman/skills/flight-pickup-tracker)
- [OpenSky Network API](https://opensky-network.org/api)
- [AirLabs API](https://airlabs.co/api/v9)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON status outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May schedule follow-up checks and should use confirmed pickup address, flight code, destination airport, and origin airport when monitoring.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
