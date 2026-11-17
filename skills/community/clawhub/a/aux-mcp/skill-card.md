## Description:

AUX - Spotify for your AI. Vibe DJ, roast cards, party rooms, and auto-DJ via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brian-mwirigi](https://clawhub.ai/user/brian-mwirigi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate the AUX Spotify MCP workflow for mood-based music selection, playlist analysis, playlist roasting, party queues, weekly recaps, and playback-oriented DJ actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned spotify-aux npm package that handles Spotify credentials and local OAuth tokens.

Mitigation: Install only if the publisher and npm package are trusted; prefer a pinned, reviewed package version before login or MCP registration.

Risk: The package receives Spotify app credentials, manages local OAuth tokens, and may run local helper services for AutoDJ or party hosting.

Mitigation: Use trusted local environments, avoid exposing client secrets or token files, and stop helper services when they are not needed.

## Reference(s):

- [AUX homepage](https://brianmunene.me/aux-mcp)
- [ClawHub skill listing](https://clawhub.ai/brian-mwirigi/skills/aux-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/brian-mwirigi)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface ASCII cards returned by AUX MCP tools; playback features require Spotify Premium and an active device.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
