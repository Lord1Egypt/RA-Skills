## Description:

Companion plugin for ClawVision that adds PDF export, OG image generation, and optional Telegram sharing for summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using ClawVision use this companion skill after generating a summary card to export a print-ready PDF, create a social-preview image, or share the summary to a Telegram chat or channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram sharing uses bot credentials and can expose a token if it is passed in chat, logs, or shell history.

Mitigation: Provide the bot token through an environment variable or secret manager, rotate any token already used on the command line, and restrict the bot's channel permissions.

Risk: Summary content sent to Telegram may come from untrusted sources and Telegram captions may not be fully escaped.

Mitigation: Require explicit user confirmation before sharing, avoid sending untrusted summaries until captions are escaped, and review the generated message before delivery.

## Reference(s):

- [ClawVision Plus README](references/README.md)
- [ClawVision project homepage](https://github.com/monaxamo/clawvision)
- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/clawvision-plus)

## Skill Output:

**Output Type(s):** [Files, Images, Shell commands, API calls]

**Output Format:** [PDF and PNG files, optional Telegram message, and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing ClawVision summary JSON and rendered HTML output; Telegram sharing requires a chat ID and bot token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
