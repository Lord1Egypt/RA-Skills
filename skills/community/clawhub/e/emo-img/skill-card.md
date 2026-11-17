## Description:

Send sticker/emoji images (表情包) in chat by searching a local collection or Tenor online, downloading favorites, and sending them through supported messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horisky](https://clawhub.ai/user/horisky)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw agent find, save, and send expressive sticker or emoji images in chat conversations across supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can fetch online media and arbitrary download URLs.

Mitigation: Use trusted URLs only, prefer Tenor search results, and add URL allowlisting plus file size and media type checks before broad deployment.

Risk: Unsafe file handling could write or delete files outside the intended sticker folder.

Mitigation: Constrain filenames and paths to the configured sticker directory before allowing add, download, or remove operations.

Risk: The skill can send media through messaging channels.

Mitigation: Require user confirmation before sending externally sourced or newly downloaded media.

Risk: TLS verification may be disabled as a fallback when certificate discovery fails.

Mitigation: Require a valid certificate bundle and fail closed rather than disabling certificate verification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/horisky/skills/emo-img)
- [OpenClaw](https://openclaw.ai)
- [Tenor Search API Endpoint](https://tenor.googleapis.com/v2/search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, download, list, or remove local sticker media files and return media paths or URLs for messaging tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
