## Description:

Azure Speech TTS generates local audio files from plain text or complete SSML using Azure Speech, with options for voice, format, speaking rate, pitch, style, and role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conanwhf](https://clawhub.ai/user/conanwhf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to synthesize narration or SSML-driven speech into local MP3, WAV, PCM, or OGG files and return the generated audio path to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A tampered Azure region value could send the Azure Speech key and speech text to a non-Azure host.

Mitigation: Validate or patch the region handling before installation and use only known Azure region values.

Risk: Speech text is sent to a cloud service for synthesis and may contain sensitive content.

Mitigation: Avoid sending sensitive text unless cloud processing is approved, and keep the Azure Speech key least-privileged and rotatable.

Risk: Explicit output paths can overwrite local files.

Mitigation: Choose output paths carefully and review generated paths before running synthesis commands.

## Reference(s):

- [Azure Speech TTS Cheatsheet](references/azure-speech-cheatsheet.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON summaries; generated audio files are MP3, WAV, PCM, or OGG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Azure Speech credentials and writes audio to local output paths.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
