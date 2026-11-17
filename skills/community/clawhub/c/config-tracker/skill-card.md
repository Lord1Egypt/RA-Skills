## Description:

Config Tracker automatically tracks and commits changes to OpenClaw configuration files and selected workspace Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[altaircardinal](https://clawhub.ai/user/altaircardinal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to keep Git history for configuration and selected workspace Markdown files so changes across conversation turns can be reviewed or recovered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically creates Git history for OpenClaw and workspace configuration files that may contain credentials, private endpoints, personal data, or sensitive agent instructions.

Mitigation: Review the tracked file list before installing; disable the skill or narrow workspaceFiles and openclawConfig when those files may contain sensitive data.

Risk: Automatic commits run at the start of conversation turns and can create local repositories or commit many changes without a separate confirmation step.

Mitigation: Install only when automatic history is intended, and monitor repository history or adjust enabled and cooldown settings before use.

## Reference(s):

- [Config Tracker ClawHub listing](https://clawhub.ai/altaircardinal/skills/config-tracker)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Git commits with text commit messages and console log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs automatically on the before_prompt_build hook and applies a 5 second cooldown between checks.]

## Skill Version(s):

1.0.2 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
