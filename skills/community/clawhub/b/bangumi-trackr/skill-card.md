## Description:

Manage Bangumi collections and track watch, read, game, and music progress through Bangumi OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mountlynx](https://clawhub.ai/user/mountlynx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a local Bangumi OAuth client, inspect personal account data, and update Bangumi collection or episode progress from command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Bangumi OAuth tokens may be exposed on non-Windows systems where credentials are stored under ~/.bangumi.

Mitigation: Use the skill only on machines where ~/.bangumi is private, do not share or commit those files, and revoke the Bangumi OAuth app if tokens may have been exposed.

Risk: The OAuth callback flow needs review before installation.

Mitigation: Create a dedicated Bangumi OAuth app with the documented localhost callback and review the authorization flow before entering credentials.

Risk: Collection, character, person, and episode commands can modify a user's Bangumi account.

Mitigation: Review proposed commands before execution and use read-only status, list, or progress commands first when confirming targets.

## Reference(s):

- [Command Reference](references/COMMANDS.md)
- [API Documentation](references/API.md)
- [Bangumi API v0](https://github.com/bangumi/api)
- [Bangumi OAuth App Setup](https://bgm.tv/dev/app/create)
- [ClawHub Skill Page](https://clawhub.ai/mountlynx/skills/bangumi-trackr)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and command reference text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local OAuth setup and user-invoked Bangumi account updates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
