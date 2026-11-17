## Description:

Send files such as archives, documents, images, and videos to the current Telegram chat through OpenClaw using the session's trusted chat context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzunglaviet](https://clawhub.ai/user/dzunglaviet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send a selected local file from an OpenClaw session to the active Telegram conversation. It is intended for file delivery workflows where the Telegram destination is supplied by trusted inbound session metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send any local file the agent can read to Telegram without enough path limits or sensitive-file warnings.

Mitigation: Restrict allowed directories, block sensitive paths such as keys and environment files, resolve symlinks before upload, and require explicit confirmation of the final path before sending.

Risk: A wrong or untrusted Telegram target could cause files to be sent to an unintended chat.

Mitigation: Read the Telegram target only from trusted inbound session metadata and require confirmation of the destination before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dzunglaviet/skills/better-telegram-file-sender)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown or plain text with shell command execution guidance and send-status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw in PATH, a configured Telegram gateway, a readable file path, and a trusted Telegram chat target from inbound context.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
