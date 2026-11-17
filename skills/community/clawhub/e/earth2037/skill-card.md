## Description:

Play Earth2037 using the current Account Center and bundled MCP/CLI. Inspect cities, buildings, heroes, tasks, troops and maps, then carry out player-authorized game actions. Use for Earth2037 registration, login and gameplay, not server administration or the Cocos editor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windinwing](https://clawhub.ai/user/windinwing)

### License/Terms of Use:

MIT-0

## Use Case:

Earth2037 players use the skill to inspect their accounts, characters and game state, and to carry out authorized gameplay through MCP tools or the CLI. It also supports local setup and migration to the current Account Center.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write mode permits consequential gameplay, including spending game currency, messaging, attacks and inventory changes; some low-level commands can skip previews.

Mitigation: Keep read-only mode enabled until the player authorizes specific changes. Use prepare and inspect the preview for supported actions, and ensure other writes match the player's explicit intent.

Risk: The local credential file contains passwords and tokens and is not encrypted.

Mitigation: Enter passwords only in the local interactive setup, protect the credential file and its permissions, and never share or upload it.

Risk: Entering a character can disconnect its existing mobile or browser session.

Mitigation: Explain the takeover effect and obtain authorization before connecting when existing takeover authorization is absent.

Risk: An account-service URL override could send credentials to an unintended host.

Mitigation: Keep the documented default unless the replacement host's ownership has been verified.

## Reference(s):

- [Earth2037 AI documentation](https://www.earth2037.com/ai/)
- [Setup, permissions and migration](references/SETUP.md)
- [Player workflows](references/WORKFLOWS.md)

## Skill Output:

**Output Type(s):** [JSON, Text, API Calls, Guidance]

**Output Format:** [Structured MCP/CLI results and gameplay status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results may be paginated or marked stale/partial; write mode is read-only by default.]

## Skill Version(s):

2.0.5 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
