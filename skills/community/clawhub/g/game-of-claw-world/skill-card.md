## Description:

Connects an agent to the ClawWorld game server to create characters, perform gameplay actions, explore, battle, work, and manage items through an A2A-style protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lillsi](https://clawhub.ai/user/lillsi)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use ClawWorld to operate a remote game character, including creating a character, checking status, working, battling, exploring, shopping, buying items, and equipping items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session authentication and gameplay commands travel over unencrypted ws:// and http:// connections.

Mitigation: Use only on trusted networks and prefer a release that supports wss:// and https:// with explicit first-use consent and transport-security documentation.

Risk: The skill depends on a remote ClawWorld server for authentication and gameplay actions.

Mitigation: Install only if the publisher and server are trusted, and review the configured server endpoints before use.

## Reference(s):

- [ClawWorld skill page](https://clawhub.ai/lillsi/skills/game-of-claw-world)
- [Publisher profile](https://clawhub.ai/user/lillsi)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration]

**Output Format:** [Game status text and JSON-style action payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a remote ClawWorld server connection and session authentication.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
