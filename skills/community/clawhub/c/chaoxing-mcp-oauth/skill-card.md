## Description:

Guides users through connecting Chaoxing/StudyAI MCP to WorkBuddy with OAuth2 authorization, local token refresh, mcp.json configuration, and troubleshooting for common authorization failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill to connect Chaoxing/StudyAI MCP, repair expired tokens, refresh authorization, and configure the local MCP server entry for StudyAI course tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client credentials and tokens may be stored on the local machine.

Mitigation: Prefer environment variables where practical, protect ~/.workbuddy, and revoke or rotate Chaoxing credentials if local files may be exposed.

Risk: The skill can update WorkBuddy MCP configuration.

Mitigation: Review the mcp.json changes before relying on the connector and keep backups for recovery.

Risk: Refresh behavior can run automatically or as a scheduled task.

Mitigation: Review any daemon or scheduled-task setup and disable it when persistent background refresh is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erich1566/skills/chaoxing-mcp-oauth)
- [Chaoxing authorization documentation](https://sharewh2.xuexi365.com/share/1ee530c1-4542-444e-8ef8-5f56247a26fa)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local OAuth setup, token refresh, and WorkBuddy MCP configuration updates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
