## Description:

Connect and use Fantopy's MCP server for World Cup 2026 predictions. Use when helping a user install Fantopy in OpenClaw, ChatGPT, Claude, Cursor, or another MCP client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantopy](https://clawhub.ai/user/fantopy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an MCP-capable agent to Fantopy so a human player can browse World Cup fixtures, make confirmed score predictions, create or join groups, check leaderboards, and share a public watch link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the hosted MCP service can create an anonymous or logged-in Fantopy player and store public-facing handles, predictions, group actions, and recovery or email-login state.

Mitigation: Tell users before installation that the agent connects to Fantopy's hosted MCP service, and only proceed with account, group, prediction, login, or recovery actions after the user understands the effect.

Risk: Prediction saves and group actions can submit choices the user did not intend.

Mitigation: Repeat exact fixture names, scores, and group actions before saving, then call prediction-saving or group tools only after explicit user confirmation.

Risk: Anonymous progress can be lost if the MCP session is lost before the user makes progress durable.

Mitigation: After meaningful picks or group actions, offer email login or a private recovery code so the user can recover progress.

## Reference(s):

- [Fantopy MCP homepage](https://github.com/Fantopy-ai/fantopy-mcp)
- [ClawHub skill listing](https://clawhub.ai/fantopy/skills/fantopy-mcp)
- [Hosted Fantopy MCP endpoint](https://mcp.fantopy.ai/mcp)
- [Fantopy app](https://app.fantopy.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP setup commands, public watch links, prediction summaries, and user-confirmation prompts.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
