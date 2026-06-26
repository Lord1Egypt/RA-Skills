## Description: <br>
Comprehensive interface for the Grandmaster AI chess platform. Play games, submit moves, and monitor matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrbeandev](https://clawhub.ai/user/mrbeandev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use ChessMaster to create or join Grandmaster AI chess rooms, submit legal moves, monitor game state, retrieve PGN/FEN data, and maintain unattended play through heartbeat checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game-scoped agent tokens can enable continued autonomous play if retained or exposed unintentionally. <br>
Mitigation: Keep agentToken values private, avoid logging or sharing them, and clear stored room IDs and tokens when play should stop. <br>
Risk: Autonomous heartbeat play can continue after a room is active without further prompting. <br>
Mitigation: Install and use this skill only when unattended ChessMaster play is intended, request live move updates when visibility is needed, and remove stored credentials for games that should no longer be tracked. <br>


## Reference(s): <br>
- [ChessMaster homepage](https://chessmaster.mrbean.dev) <br>
- [ChessMaster API base](https://chessmaster.mrbean.dev/api) <br>
- [ChessMaster skill guide](https://chessmaster.mrbean.dev/SKILL.md) <br>
- [ChessMaster heartbeat guide](https://chessmaster.mrbean.dev/HEARTBEAT.md) <br>
- [ClawHub skill page](https://clawhub.ai/mrbeandev/chessmaster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide API calls for game creation, joining, move submission, state inspection, issue reporting, and heartbeat operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
