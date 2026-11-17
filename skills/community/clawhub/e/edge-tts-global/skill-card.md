## Description:

Use the globally installed edge-tts command to generate Chinese or multilingual text-to-speech audio on this machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert user-provided text into speech with the globally installed edge-tts command, including Chinese or multilingual audio, Telegram voice-message style audio, and optional subtitle files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text may be sent to the online Edge TTS provider.

Mitigation: Use only non-sensitive text unless the user is comfortable sending that text to the provider.

Risk: The cleanup helper can delete arbitrary user-writable file paths.

Mitigation: Avoid cleanup on untrusted paths until it is constrained to generated files under the workspace temp directory and rejects absolute paths, parent traversal, symlinks, and non-MP3/VTT files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; generated MP3 audio files and optional VTT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temporary outputs are intended for the caller workspace temp directory and should be deleted after successful sending.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
