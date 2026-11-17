## Description:

Set the default model persistently via /default_model command with Telegram interactive picker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkyotnfjfbjnknh](https://clawhub.ai/user/jkyotnfjfbjnknh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use this skill to view or update the persistent default model for new sessions through the /default_model command. Telegram users can select a provider and model through an interactive picker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized access to /default_model can change the persistent default model used by new OpenClaw sessions.

Mitigation: Treat the command as administrative and restrict use to trusted authorized senders.

Risk: A full provider/model argument may be accepted even when it is not present in the local model catalog.

Mitigation: Confirm model identifiers before setting them, especially when entering provider/model values manually.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Markdown-formatted chat text and persistent OpenClaw configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates agents.defaults.model.primary for new OpenClaw sessions; the current session model is unchanged.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
