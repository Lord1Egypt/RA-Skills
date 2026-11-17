## Description:

Handle audio messages as commands by transcribing WAV, PCM, or MP3 files with iFlytek Speed Transcription, then executing the transcription as the command or using it as context for an accompanying text command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let audio files drive agent workflows: audio-only messages become commands, while audio plus text messages use the transcript as context for the text instruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio content can be converted into agent commands.

Mitigation: Show the transcript and ask for explicit user confirmation before executing any command derived from audio.

Risk: Long audio-plus-text results can be saved and uploaded.

Mitigation: Ask before uploading results, and avoid private recordings, credentials, or sensitive business content unless the transcription and upload services are trusted and access-controlled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/skills/audio-command-handler)
- [Publisher Profile](https://clawhub.ai/user/smallkeyboy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus text or JSON output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write HTML files for long results and return uploaded URLs when the uploader skill is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
