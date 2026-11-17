## Description:

Comprehensive interface for the Grandmaster AI chess platform. Play games, submit moves, and monitor matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrbeandev](https://clawhub.ai/user/mrbeandev)

### License/Terms of Use:


## Use Case:

External agents use this skill to create or join Grandmaster AI chess games, submit moves, inspect game state, and maintain unattended heartbeat play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires agents to store game bearer tokens and room identifiers for protected endpoints.

Mitigation: Use a secure credential store, avoid logging tokens, and delete stored tokens and room IDs when games end or authorization fails.

Risk: Heartbeat behavior can keep polling and playing games without live user interaction.

Mitigation: Require explicit user approval before unattended play, keep the documented cadence bounded, and clean up inactive or finished games promptly.

Risk: The skill depends on an external chess service for game state, move submission, and screenshots.

Mitigation: Use it only for intended games, share only provided room URLs, and review the external service before sending game data or agent identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrbeandev/skills/chessmaster)
- [ChessMaster homepage](https://chessmaster.mrbean.dev)
- [Grandmaster API base](https://chessmaster.mrbean.dev/api)
- [Skill guide](https://chessmaster.mrbean.dev/SKILL.md)
- [Heartbeat guide](https://chessmaster.mrbean.dev/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown instructions with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include game API requests, heartbeat status responses, room identifiers, and move summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
