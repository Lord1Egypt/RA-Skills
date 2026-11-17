## Description:

Play local or network audio/video files with PotPlayer, including playback controls, playlists, fullscreen playback, subtitles, and device access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isaiah5818](https://clawhub.ai/user/isaiah5818)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting Windows users can generate PotPlayer launch commands to play local media or network streams, manage playlists, control playback options, and load subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes webcam and screen-capture commands without clear consent or scoping.

Mitigation: Review or remove the webcam and screen-capture examples, and require explicit user confirmation before any camera input or screen recording command is run.

Risk: The skill can open remote media streams.

Mitigation: Require explicit confirmation before opening remote streams, and ask the user to verify the stream source before launching PotPlayer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isaiah5818/skills/ctrl-potplayer)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that launch local files, remote streams, webcam input, or screen capture through PotPlayer.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
