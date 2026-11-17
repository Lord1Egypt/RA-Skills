## Description:

Converts workspace files into Telegram-downloadable PDF or ZIP attachments when a user asks to receive or download generated files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awalesagar](https://clawhub.ai/user/awalesagar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to package generated or existing workspace files as downloadable Telegram attachments, especially Markdown reports that need PDF conversion or grouped files that need ZIP packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested files may be sent through Telegram/OpenClaw MEDIA, including sensitive workspace files if the path is not reviewed.

Mitigation: Confirm the exact file path and sensitivity before use, and send only intended non-sensitive artifacts.

Risk: The workflow may install mdpdf with pip during delivery without a pinned package version.

Mitigation: Prefer a controlled environment with mdpdf preinstalled or pinned before enabling the skill.

Risk: Broad trigger phrases could invoke file delivery behavior unexpectedly.

Mitigation: Require explicit confirmation of the file path and intended delivery before running conversion or delivery commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awalesagar/skills/axi-send-file)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown with inline bash commands and MEDIA file delivery lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces downloadable file artifacts such as PDF or ZIP attachments from workspace files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
