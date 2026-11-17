## Description:

Quick diagnosis and repair for Discord bot, Gateway, OAuth token, and legacy config issues. Checks connectivity, token expiration, and cleans up old Clawdis artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhillock](https://clawhub.ai/user/jhillock)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose Discord bot, Clawdbot gateway, OAuth token, and legacy Clawdis configuration issues, and to receive repair commands or cleanup guidance when fixes are requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair actions may install npm packages, restart the gateway, remove an old launchd service, or move a legacy ~/.clawdis directory.

Mitigation: Review proposed --fix actions before running them, and keep backups of legacy configuration before cleanup.

Risk: OAuth reauthentication guidance may invoke npx to fetch a package.

Mitigation: Use a trusted local or pinned clawdbot package for reauthentication when possible.

## Reference(s):

- [Discord Doctor on ClawHub](https://clawhub.ai/jhillock/skills/discord-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, gateway restart, OAuth reauthentication, and legacy Clawdis cleanup actions when run with --fix.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
