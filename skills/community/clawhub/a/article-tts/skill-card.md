## Description:

Converts article photos or plain text into natural audio with OCR, Microsoft Edge TTS, English/Chinese support, configurable voice and speed, and optional sentence splitting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54meteor](https://clawhub.ai/user/54meteor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to turn article images or supplied text into listenable audio, then send the generated audio through the active chat channel or save it locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR text and generated audio can be sent through the active chat channel.

Mitigation: Keep text confirmation enabled for sensitive images and use only chat channels appropriate for the content.

Risk: The TTS dependency can be downloaded at runtime through an unpinned edge-tts invocation.

Mitigation: Prefer a pinned or preinstalled edge-tts version in shared or controlled environments.

Risk: Temporary OCR and audio files may expose content in shared environments.

Mitigation: Use private per-run output directories and remove generated files when they are no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime artifacts include original_text.md and MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese OCR/TTS, configurable speed and voice, optional confirmation, and optional sentence-level audio splitting.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
